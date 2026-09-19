"""
A harness that measurably improves itself from its own execution traces.

Real LLM calls (deepseek-flash), real REPL, real measurement. The improvement
is not asserted — it is A/B tested: run a task set with a baseline prompt, mine
the failures for a lesson, then re-run the SAME tasks with the lesson appended
and compare. The demo prints whichever result actually happens, including "no
improvement" or a regression.

The real version of this idea has a name and a paper: **Meta-Harness: End-to-End
Optimization of Model Harnesses** (arXiv 2603.28052, Lee/Nair/Zhang/Lee/Khattab/Finn,
Stanford/MIT/KRAFTON, 2026-03-30). It runs an agentic proposer that reads the source
code, scores, and execution traces of every prior candidate harness through a
filesystem, and reports +7.7 points over a SOTA context manager with 4x fewer context
tokens, +4.7 points on 200 IMO-level problems across five held-out models, and
harnesses that surpass the best hand-engineered baselines on TerminalBench-2. Its
stated reason for working is the same one this file leans on: give the optimizer raw
traces, because existing text optimizers "compress feedback too aggressively."
This file is that loop in miniature. Cite the paper, not this file.

Result when run on 2026-09-10 (deepseek-flash), 3 runs of 3: the baseline scored 4/4 with
zero REPL errors on two different task sets, so there was nothing to mine and the
A/B never fired. That is a real finding worth saying on camera — a code-writing
agent with a REPL is already reliable on tasks like these, and the self-improvement
machinery has nothing to bite on. The mining -> re-run path is therefore CODE
COMPLETE BUT UNEXERCISED. To actually demo it, use a task set this model genuinely
fails (harder reasoning, strict output contracts, or a weaker model) — and if it
still passes, report that instead of rigging the tasks to fail.

That negative result is worth saying out loud rather than hiding: it is exactly why
Meta-Harness evaluates on IMO-level problems and TerminalBench-2 instead of
arithmetic. Trace mining needs traces worth mining.

The other verified point of contact: Tufa Labs' Duck harness keeps context bounded by
evicting oldest messages, and its authors kept the harness minimal.
(tufalabs.ai/research/duck-harness/)

Setup:  export DEEPSEEK_API_KEY=<key>   (legacy DEEPSEEK_API_PATAPI still works)
"""

import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from typing import Callable, List, Optional

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _config import DEEPSEEK_MODEL, deepseek_key

API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = DEEPSEEK_MODEL
MAX_TOKENS = 2000  # reasoning model: needs room before content appears

BASE_PROMPT = """You solve problems by writing Python.
Reply with exactly one ```python block. The code runs and you see its stdout.
When confident, reply FINAL: <answer> with no code block."""


@dataclass
class Trace:
    """One task attempt. This is the raw material for mining."""
    task: str
    answer: Optional[str]
    correct: bool
    turns: int
    repl_errors: int
    error_text: str = ""
    completion_tokens: int = 0


@dataclass
class Task:
    prompt: str
    check: Callable[[str], bool]


def run_python(code: str, timeout: int = 10) -> tuple:
    path = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write(code)
            path = f.name
        p = subprocess.run([sys.executable, path], capture_output=True,
                           text=True, timeout=timeout)
        out = p.stdout if p.returncode == 0 else (p.stderr or p.stdout)
        return p.returncode == 0, out.strip()
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout}s"
    except Exception as e:
        return False, str(e)
    finally:
        if path:
            try:
                os.unlink(path)
            except OSError:
                pass


def extract_code(text: str) -> Optional[str]:
    m = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.S)
    return m.group(1).strip() if m else None


class Harness:
    def __init__(self, api_key: str, system_prompt: str):
        self.api_key = api_key
        self.system_prompt = system_prompt

    def _call(self, messages: List[dict]) -> tuple:
        r = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {self.api_key}",
                     "Content-Type": "application/json"},
            json={"model": MODEL, "messages": messages, "max_tokens": MAX_TOKENS},
            timeout=120,
        )
        r.raise_for_status()
        body = r.json()
        choice = body["choices"][0]
        content = choice["message"].get("content") or ""
        return content, body.get("usage", {}).get("completion_tokens", 0)

    def attempt(self, task: Task, max_turns: int = 5) -> Trace:
        messages = [{"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": task.prompt}]
        errors, tokens, last_error = 0, 0, ""

        for turn in range(1, max_turns + 1):
            reply, used = self._call(messages)
            tokens += used
            messages.append({"role": "assistant", "content": reply})

            if "FINAL:" in reply:
                answer = reply.split("FINAL:", 1)[1].strip()
                return Trace(task.prompt, answer, task.check(answer), turn,
                             errors, last_error, tokens)

            code = extract_code(reply)
            if not code:
                messages.append({"role": "user",
                                 "content": "One ```python block, or FINAL: <answer>."})
                continue

            ok, out = run_python(code)
            if not ok:
                errors += 1
                last_error = out.strip().splitlines()[-1] if out.strip() else "error"
            messages.append({"role": "user", "content": f"stdout:\n{out}"})

        return Trace(task.prompt, None, False, max_turns, errors, last_error, tokens)


def mine(traces: List[Trace], api_key: str) -> Optional[str]:
    """Ask the model to read its own failures and write one rule to fix them.

    This is the actual trace-mining step: failures in, a prompt amendment out.
    Returns None when there is nothing to learn.
    """
    failures = [t for t in traces if not t.correct or t.repl_errors]
    if not failures:
        return None

    report = "\n".join(
        f"- task: {t.task[:90]}\n  correct={t.correct} turns={t.turns} "
        f"repl_errors={t.repl_errors} last_error={t.error_text[:90]!r}"
        for t in failures
    )
    messages = [
        {"role": "system", "content":
         "You tune the system prompt of a code-writing agent. Read its failed "
         "traces and reply with ONE imperative sentence to append to its prompt "
         "that would prevent these failures. No preamble, just the sentence."},
        {"role": "user", "content": f"Failed traces:\n{report}"},
    ]
    r = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": MODEL, "messages": messages, "max_tokens": MAX_TOKENS},
        timeout=120,
    )
    r.raise_for_status()
    lesson = (r.json()["choices"][0]["message"].get("content") or "").strip()
    return lesson or None


def score(traces: List[Trace]) -> dict:
    n = len(traces)
    return {
        "solved": sum(t.correct for t in traces),
        "n": n,
        "errors": sum(t.repl_errors for t in traces),
        "turns": sum(t.turns for t in traces) / n if n else 0,
        "tokens": sum(t.completion_tokens for t in traces),
    }


def report(label: str, s: dict):
    print(f"  {label:<10} solved {s['solved']}/{s['n']}   "
          f"repl_errors {s['errors']}   avg_turns {s['turns']:.2f}   "
          f"completion_tokens {s['tokens']}")


# Tasks with programmatic checks — no LLM grades itself here.
#
# These are deliberately hard enough that a first pass may fail: each has a
# precise output format or an edge case that is easy to get subtly wrong. The
# point is to give trace mining something real to find. They are NOT rigged to
# fail — every one is solvable, and if the baseline aces them the demo says so.
TASKS = [
    Task("Sum every number from 1 to 100 divisible by both 2 and 3. "
         "Answer with the bare integer and nothing else.",
         lambda a: a.strip().rstrip(".") == "816"),
    Task("Count distinct characters in 'harness engineering', spaces included. "
         "Answer with the bare integer and nothing else.",
         lambda a: a.strip().rstrip(".") == str(len(set("harness engineering")))),
    Task("A year is a leap year if divisible by 4, except centuries, unless "
         "divisible by 400. How many leap years strictly between 1800 and 2400? "
         "Answer with the bare integer and nothing else.",
         lambda a: a.strip().rstrip(".") == str(sum(
             1 for y in range(1801, 2400)
             if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)))),
    Task("Report the median of [5,3,9,1,7,2] as a decimal. "
         "Answer with the bare number and nothing else.",
         lambda a: a.strip().rstrip(".") in ("4.0", "4")),
]


def main():
    key = deepseek_key()
    if not key:
        sys.exit("Set DEEPSEEK_API_KEY (or legacy DEEPSEEK_API_PATAPI)")

    print("=" * 72)
    print("Self-improvement, A/B tested against the same task set")
    print(f"model={MODEL}  tasks={len(TASKS)}  checks are programmatic")
    print("=" * 72)

    print("\n[1] baseline run")
    before = [Harness(key, BASE_PROMPT).attempt(t) for t in TASKS]
    for t in before:
        print(f"  {'ok ' if t.correct else 'FAIL'} {t.task[:58]:<58} "
              f"turns={t.turns} errors={t.repl_errors}")
    s_before = score(before)

    print("\n[2] mining traces for a lesson")
    lesson = mine(before, key)
    if not lesson:
        print("  nothing failed — no lesson to learn, nothing to A/B test.")
        report("baseline", s_before)
        return 0
    print(f"  learned: {lesson}")

    print("\n[3] re-running the SAME tasks with the lesson appended")
    after = [Harness(key, BASE_PROMPT + "\n" + lesson).attempt(t) for t in TASKS]
    for t in after:
        print(f"  {'ok ' if t.correct else 'FAIL'} {t.task[:58]:<58} "
              f"turns={t.turns} errors={t.repl_errors}")
    s_after = score(after)

    print("\n" + "=" * 72)
    report("before", s_before)
    report("after", s_after)

    d_solved = s_after["solved"] - s_before["solved"]
    d_errors = s_after["errors"] - s_before["errors"]
    if d_solved > 0 or (d_solved == 0 and d_errors < 0):
        verdict = "improved"
    elif d_solved == 0 and d_errors == 0:
        verdict = "no measurable change"
    else:
        verdict = "REGRESSED"
    print(f"\n  verdict: {verdict}  (solved {d_solved:+d}, repl_errors {d_errors:+d})")
    print("  One run of 4 tasks is an anecdote, not evidence. Repeat across")
    print("  many tasks and seeds before claiming a harness improves itself.")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
