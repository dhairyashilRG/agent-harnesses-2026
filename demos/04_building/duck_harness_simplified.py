"""
A real code-writing agent, in the style of Tufa Labs' Duck harness.

This calls a live LLM (deepseek-flash), executes the Python it writes in a
subprocess REPL, feeds the output back, and loops until the model reports an
answer. Nothing here is mocked — if the model writes bad code, you watch it fail
and fix it, which is the interesting part to show an audience.

Duck's real design (tufalabs.ai/research/duck-harness/, verified 2026-07-17):
  - built on Qwen 3.6 27B FP8
  - minimal coding harness with a Python REPL, game perception through images
  - observations arrive as Python variables, inspected via tool calls
  - "infinite play via eviction": pop oldest messages, keep system prompt +
    recent history, so context never runs out
  - reported an order of magnitude cheaper per game than a compared approach

This file borrows the shape (LLM writes code -> REPL -> observe -> iterate) and
the eviction idea. It is not Duck, does not play ARC, and does not reproduce
Duck's score. Duck scored 1.21% on the ARC-AGI-3 Milestone 1 leaderboard.

Setup:  export DEEPSEEK_API_KEY=<key>   (legacy DEEPSEEK_API_PATAPI still works)
Run:    python3 demos/04_building/duck_harness_simplified.py
"""

import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from typing import List, Optional

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _config import DEEPSEEK_MODEL, deepseek_key

API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = DEEPSEEK_MODEL  # deepseek-flash; confirmed by a live run 2026-09-10

# deepseek-flash is a reasoning model: it spends completion tokens on
# reasoning_content before emitting any content. A small max_tokens returns an
# empty string with finish_reason="length". Budget accordingly.
MAX_TOKENS = 2000

SYSTEM_PROMPT = """You solve problems by writing Python.

Reply with exactly one Python code block per turn:

```python
print(...)
```

The code runs immediately and you see its stdout. Print what you need to see.
When you are confident, reply with FINAL: <answer> and no code block.
Keep code short. You have no network access."""


@dataclass
class ExecResult:
    ok: bool
    output: str
    seconds: float


class REPL:
    """Runs model-written Python in a subprocess with a timeout."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.runs = 0

    def run(self, code: str) -> ExecResult:
        self.runs += 1
        start = time.time()
        path = None
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
                f.write(code)
                path = f.name
            proc = subprocess.run(
                [sys.executable, path],
                capture_output=True, text=True, timeout=self.timeout,
            )
            out = proc.stdout if proc.returncode == 0 else (proc.stderr or proc.stdout)
            return ExecResult(proc.returncode == 0, out.strip(), time.time() - start)
        except subprocess.TimeoutExpired:
            return ExecResult(False, f"timed out after {self.timeout}s", float(self.timeout))
        except Exception as e:
            return ExecResult(False, str(e), time.time() - start)
        finally:
            if path:
                try:
                    os.unlink(path)
                except OSError:
                    pass


def extract_code(text: str) -> Optional[str]:
    m = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.S)
    return m.group(1).strip() if m else None


class CodeAgent:
    def __init__(self, api_key: str, keep_turns: int = 6):
        self.api_key = api_key
        self.repl = REPL()
        self.messages: List[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.keep_turns = keep_turns  # Duck-style eviction window
        self.prompt_tokens = 0
        self.completion_tokens = 0

    def _evict(self):
        """Duck's trick: keep the system prompt, drop the oldest turns."""
        if len(self.messages) > self.keep_turns + 1:
            self.messages = [self.messages[0]] + self.messages[-self.keep_turns:]

    def _call(self) -> str:
        r = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {self.api_key}",
                     "Content-Type": "application/json"},
            json={"model": MODEL, "messages": self.messages, "max_tokens": MAX_TOKENS},
            timeout=120,
        )
        r.raise_for_status()
        body = r.json()
        usage = body.get("usage", {})
        self.prompt_tokens += usage.get("prompt_tokens", 0)
        self.completion_tokens += usage.get("completion_tokens", 0)
        choice = body["choices"][0]
        if choice.get("finish_reason") == "length" and not choice["message"].get("content"):
            raise RuntimeError(
                "Model hit the token limit before emitting content — raise MAX_TOKENS."
            )
        return choice["message"]["content"]

    def solve(self, task: str, max_turns: int = 6) -> Optional[str]:
        print("=" * 72)
        print(f"TASK: {task}")
        print(f"model={MODEL}  eviction: system prompt + last {self.keep_turns} messages")
        print("=" * 72)

        self.messages.append({"role": "user", "content": task})

        for turn in range(1, max_turns + 1):
            print(f"\n--- turn {turn}/{max_turns} " + "-" * 50)
            reply = self._call()
            self.messages.append({"role": "assistant", "content": reply})

            if "FINAL:" in reply:
                answer = reply.split("FINAL:", 1)[1].strip()
                print(f"FINAL: {answer}")
                return answer

            code = extract_code(reply)
            if not code:
                print("(no code block; nudging)")
                self.messages.append({
                    "role": "user",
                    "content": "Reply with one ```python block, or FINAL: <answer>.",
                })
                self._evict()
                continue

            print("model wrote:")
            for line in code.splitlines():
                print(f"  | {line}")

            res = self.repl.run(code)
            status = "ok" if res.ok else "ERROR"
            print(f"\nREPL [{status}] {res.seconds:.2f}s:")
            for line in (res.output or "(no output)").splitlines()[:15]:
                print(f"  > {line}")

            self.messages.append({"role": "user", "content": f"stdout:\n{res.output}"})
            self._evict()

        print("\nhit turn limit without FINAL")
        return None


def main():
    key = deepseek_key()
    if not key:
        sys.exit("Set DEEPSEEK_API_KEY (or legacy DEEPSEEK_API_PATAPI)")

    agent = CodeAgent(key)
    task = (
        "Find the sum of all numbers from 1 to 100 that are even AND divisible by 3. "
        "Verify by printing the numbers you summed."
    )
    answer = agent.solve(task)

    print("\n" + "=" * 72)
    print(f"answer            : {answer}")
    print(f"REPL executions   : {agent.repl.runs}")
    print(f"tokens            : {agent.prompt_tokens} prompt + "
          f"{agent.completion_tokens} completion")

    # Independent check — the harness verifying the agent, not trusting it.
    truth = sum(n for n in range(1, 101) if n % 2 == 0 and n % 3 == 0)
    ok = answer is not None and str(truth) in answer
    print(f"ground truth      : {truth}")
    print(f"agent correct     : {'YES' if ok else 'NO'}")
    print("=" * 72)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
