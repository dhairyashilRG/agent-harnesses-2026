"""
Same model, two harnesses: a Wordle A/B.

The series' thesis, reproduced live on a game everyone knows. Two runs, same model,
same word, same guess budget:

  A — NAKED:     the model plays through plain chat. It sees the feedback as text and
                 replies with its next guess. No tools, no code, no structure.
  B — HARNESSED: the model writes Python per turn. The harness runs it in a subprocess
                 REPL with the full word list and guess history preloaded, so the model
                 can COMPUTE the remaining candidates instead of vibing. Plus the layers
                 from duck_harness_simplified: eviction, fail-loud calls, and independent
                 verification (the harness scores every guess itself — the model's
                 self-report is never trusted).

At the end, both runs get an RHAE-style efficiency score:

    score = min(1.15, (human_baseline_guesses / guesses_used) ** 2), 0 if unsolved

which is the same squared-penalty shape as ARC-AGI-3's metric
(demos/06_evaluation/arc_agi3_runner.py) — solving is necessary, efficiency is the axis.

HONESTY NOTES (read before recording):
- HUMAN_BASELINE_GUESSES = 4 is this demo's assumed baseline, chosen because commonly
  cited Wordle averages hover around 4. It is a demo parameter, NOT an official
  statistic — verify or hedge before quoting a number on camera.
- One round is an anecdote. Run --rounds 5 and report the real tally, including any
  round the naked model wins. "Usually, not always" is the claim this demo supports.
- Everything except the model calls is deterministic and offline: the word list is
  embedded, feedback is computed by the harness, and no LLM grades itself.

Setup:  export DEEPSEEK_API_KEY=<key>   (legacy DEEPSEEK_API_PATAPI still works)
Run:    python3 demos/04_building/wordle_ab.py [--rounds N] [--seed N] [--answer WORD]
Test:   python3 demos/04_building/wordle_ab.py --selftest   (offline, no API)
"""

import argparse
import os
import random
import re
import subprocess
import sys
import tempfile
from collections import Counter
from typing import List, Optional, Tuple

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _config import DEEPSEEK_MODEL, deepseek_key

API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = DEEPSEEK_MODEL
MAX_TOKENS = 16000         # reasoning model: budget for thinking BEFORE any content.
                           # 2000 was enough in July, not in September, and 6000 still was
                           # not: the naked run reasons hardest on its LAST guesses, when
                           # the history is longest. Deducing a word from three colour
                           # patterns is exactly the kind of search a model does in tokens
                           # instead of in code -- which is the point of run B.
                           # This is Ep 7 Card 1; the guard below is why it is loud.
MAX_GUESSES = 6
MAX_CODE_TURNS_PER_GUESS = 2   # bound cost: at most 2 REPL runs before each guess
HUMAN_BASELINE_GUESSES = 4     # demo baseline — see honesty notes in the docstring

# ~230 common five-letter words. Embedded so the demo is deterministic and offline
# apart from the model calls. Answers are drawn from this same list.
WORDS = """
about above abuse actor acute adapt admit adopt after again agent agree ahead alarm
album alert alike alive allow alone along alter anger angle angry apart apple apply
arena argue arise armor array aside asset audio audit avoid awake award aware badly
baker bases basic beach began begin being below bench birth black blame blind block
blood board boost booth bound brain brand bread break breed brief bring broad broke
brown build built buyer cable calif carry catch cause chain chair chart chase cheap
check chest chief child china chose civil claim class clean clear click clock close
coach coast could count court cover craft crash cream crime cross crowd crown curve
cycle daily dance dated dealt death debut delay depth doing doubt dozen draft drama
drawn dream dress drill drink drive drove dying eager early earth eight elite empty
enemy enjoy enter entry equal error event every exact exist extra faith false fault
fiber field fifth fifty fight final first fixed flash fleet floor fluid focus force
forth forty forum found frame frank fraud fresh front fruit fully funny giant given
glass globe going grace grade grand grant grass great green gross group grown guard
guess guest guide happy harsh heart heavy hence horse hotel house human ideal image
index inner input issue joint judge known label large laser later laugh layer learn
lease least leave legal level light limit lives local logic loose lower lucky lunch
lying magic major maker march match maybe mayor meant media metal might minor minus
mixed model money month moral motor mount mouse mouth movie music needs never newly
night noise north noted novel nurse occur ocean offer often order other ought paint
panel paper party peace phase phone photo piece pilot pitch place plain plane plant
plate point pound power press price pride prime print prior prize proof proud prove
queen quick quiet quite radio raise range rapid ratio reach ready refer right rival
river robot roman rough round route royal rural scale scene scope score sense serve
seven shall shape share sharp sheet shelf shell shift shirt shock shoot short shown
sight since sixth sixty sized skill sleep slide small smart smile smoke solid solve
sorry sound south space spare speak speed spend spent split spoke sport staff stage
stake stand start state steam steel stick still stock stone stood store storm story
strip stuck study stuff style sugar suite super sweet table taken taste taxes teach
thank theft theme there these thick thing think third those three threw throw tight
timer today topic total touch tough tower track trade train treat trend trial tried
tries truck truly trust truth twice under undue union unity until upper upset urban
usage usual valid value video virus visit vital voice waste watch water wheel where
which while white whole whose woman women world worry worse worst worth would wound
write wrong wrote young youth
""".split()


# --- game mechanics (harness-side, deterministic, never delegated to the model) ---

def feedback(guess: str, answer: str) -> str:
    """Standard Wordle scoring with duplicate handling. G=green Y=yellow B=gray."""
    res = ["B"] * 5
    counts = Counter()
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            res[i] = "G"
        else:
            counts[a] += 1
    for i, g in enumerate(guess):
        if res[i] == "B" and counts[g] > 0:
            res[i] = "Y"
            counts[g] -= 1
    return "".join(res)


def candidates(history: List[Tuple[str, str]]) -> List[str]:
    """Words still consistent with every (guess, feedback) pair. Used for reporting
    only — in run B the model writes its OWN filter; this is the harness's check."""
    return [w for w in WORDS if all(feedback(g, w) == f for g, f in history)]


def rhae_style(guesses_used: Optional[int]) -> float:
    if guesses_used is None:
        return 0.0
    return min(1.15, (HUMAN_BASELINE_GUESSES / guesses_used) ** 2)


# --- shared plumbing (same shape as duck_harness_simplified) ---

class BudgetExhausted(RuntimeError):
    """The model spent its whole completion budget reasoning and emitted nothing.

    A harness that is *doing* a job should fail loudly here — that is the lesson in
    Episode 4, Step 2, and `duck_harness_simplified.py` does exactly that. This file is
    not doing a job; it is a measuring rig comparing two runs. A run that burns its
    budget without producing a guess has failed that turn, and failing a turn is a
    result. Aborting the whole comparison because one side did badly would be the rig
    hiding its own finding.
    """

    def __init__(self, message: str, tokens: int = 0, completion: int = 0,
                 reasoning=None):
        super().__init__(message)
        self.tokens = tokens
        self.completion = completion      # what it actually spent
        self.reasoning = reasoning        # how much of that was reasoning


def call_model(key: str, messages: List[dict]) -> Tuple[str, int]:
    r = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": MODEL, "messages": messages, "max_tokens": MAX_TOKENS},
        timeout=120,
    )
    r.raise_for_status()
    body = r.json()
    choice = body["choices"][0]
    if choice.get("finish_reason") == "length" and not choice["message"].get("content"):
        u = body.get("usage", {}) or {}
        reasoning = (u.get("completion_tokens_details") or {}).get("reasoning_tokens", "?")
        raise BudgetExhausted(
            f"spent {u.get('completion_tokens')} of {MAX_TOKENS} completion tokens "
            f"({reasoning} of them reasoning) without emitting a guess",
            tokens=u.get("prompt_tokens", 0) + u.get("completion_tokens", 0),
            completion=u.get("completion_tokens", 0) or 0,
            reasoning=reasoning if isinstance(reasoning, int) else None,
        )
    usage = body.get("usage", {})
    tokens = usage.get("prompt_tokens", 0) + usage.get("completion_tokens", 0)
    return choice["message"]["content"] or "", tokens


# Every turn either side takes, in order. The printed transcript is for a human
# watching it happen; this is for anything that needs to replay the run afterwards —
# the numbers on screen in the ad cut come from here rather than from a recreation.
TRACE: List[dict] = []
TRACE_ROUND = 0


def trace(run: str, event: str, **kw):
    TRACE.append({"round": TRACE_ROUND, "run": run, "event": event, **kw})


def run_python(code: str, timeout: int = 10) -> str:
    path = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write(code)
            path = f.name
        p = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        out = p.stdout if p.returncode == 0 else (p.stderr or p.stdout)
        return out.strip()
    except subprocess.TimeoutExpired:
        return f"timed out after {timeout}s"
    finally:
        if path:
            try:
                os.unlink(path)
            except OSError:
                pass


def parse_guess(text: str) -> Optional[str]:
    m = re.search(r"GUESS:\s*([a-zA-Z]{5})\b", text)
    if m:
        return m.group(1).lower()
    return None


def extract_code(text: str) -> Optional[str]:
    m = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.S)
    return m.group(1).strip() if m else None


# --- Run A: the naked model ---

NAKED_PROMPT = """You are playing Wordle. Guess the secret 5-letter word in at most 6 guesses.
After each guess you get feedback per letter: G = right letter right spot,
Y = letter in the word but wrong spot, B = letter not in the word (after greens/yellows).
Reply with exactly one line: GUESS: <word>"""


def play_naked(key: str, answer: str, verbose: bool = True) -> dict:
    messages = [{"role": "system", "content": NAKED_PROMPT},
                {"role": "user", "content": "Start. Make your first guess."}]
    history, tokens, nudges = [], 0, 0
    while len(history) < MAX_GUESSES:
        try:
            reply, used = call_model(key, messages)
        except BudgetExhausted as e:
            tokens += e.tokens
            nudges += 1
            trace("A", "budget_exhausted", guess_no=len(history) + 1,
                  completion=e.completion, reasoning=e.reasoning, max_tokens=MAX_TOKENS)
            if verbose:
                print(f"    A guess {len(history) + 1}: no guess — {e}")
            if nudges > 3:
                break
            messages.append({"role": "user", "content":
                             "Answer in one short line: GUESS: <word>. Do not deliberate."})
            continue
        tokens += used
        messages.append({"role": "assistant", "content": reply})
        guess = parse_guess(reply)
        if not guess or guess not in WORDS:
            nudges += 1
            if nudges > 3:
                break
            messages.append({"role": "user", "content":
                             "Invalid. Reply with exactly: GUESS: <a valid common 5-letter word>"})
            continue
        fb = feedback(guess, answer)          # harness scores it — never the model
        history.append((guess, fb))
        left = len(candidates(history))
        trace("A", "guess", guess_no=len(history), guess=guess, feedback=fb,
              left=left, tokens=tokens)
        if verbose:
            print(f"    A guess {len(history)}: {guess} -> {fb}   ({left} candidates remain)")
        if fb == "GGGGG":
            return {"solved": True, "guesses": len(history), "tokens": tokens, "history": history}
        messages.append({"role": "user", "content": f"Feedback for {guess}: {fb}. Next guess."})
    return {"solved": False, "guesses": None, "tokens": tokens, "history": history}


# --- Run B: same model, real harness ---

HARNESS_PROMPT = """You are playing Wordle (secret 5-letter word, at most 6 guesses).
Feedback per letter: G = right spot, Y = in word wrong spot, B = not in word.

You solve this by WRITING PYTHON, not by intuition. Each turn, either:
1. Reply with one ```python code block. It runs immediately with these variables
   predefined: WORDS (list of all valid words) and HISTORY (list of (guess, feedback)
   tuples so far). Write code that filters WORDS to the candidates consistent with
   HISTORY and print what you need to see. Remember duplicate-letter rules.
2. Or reply with exactly: GUESS: <word>  (must be a word from WORDS)

Compute before you guess. Keep code short."""


def play_harnessed(key: str, answer: str, keep_turns: int = 8, verbose: bool = True) -> dict:
    messages = [{"role": "system", "content": HARNESS_PROMPT},
                {"role": "user", "content": "Start. Analyze or guess."}]
    history, tokens, repl_runs = [], 0, 0

    def evict():
        # Duck's trick: keep the system prompt, drop the oldest turns. The game
        # state itself survives eviction because HISTORY is re-injected into the
        # REPL preamble every run — state lives in the harness, not the transcript.
        nonlocal messages
        if len(messages) > keep_turns + 1:
            messages = [messages[0]] + messages[-keep_turns:]

    while len(history) < MAX_GUESSES:
        code_turns = 0
        stalls = 0
        while True:
            try:
                reply, used = call_model(key, messages)
            except BudgetExhausted as e:
                tokens += e.tokens
                stalls += 1
                trace("B", "budget_exhausted", guess_no=len(history) + 1,
                      completion=e.completion, reasoning=e.reasoning, max_tokens=MAX_TOKENS)
                if verbose:
                    print(f"    B guess {len(history) + 1}: no reply — {e}")
                if stalls > 3:
                    return {"solved": False, "guesses": None, "tokens": tokens,
                            "repl_runs": repl_runs, "history": history}
                messages.append({"role": "user", "content":
                                 "Reply with one short ```python block, or GUESS: <word>."})
                evict()
                continue
            tokens += used
            messages.append({"role": "assistant", "content": reply})
            guess = parse_guess(reply)
            if guess:
                break
            code = extract_code(reply)
            if code and code_turns < MAX_CODE_TURNS_PER_GUESS:
                code_turns += 1
                repl_runs += 1
                preamble = f"WORDS = {WORDS!r}\nHISTORY = {history!r}\n"
                out = run_python(preamble + code)
                trace("B", "repl", guess_no=len(history) + 1, code=code, out=out[:1500])
                messages.append({"role": "user", "content": f"stdout:\n{out[:1500]}"})
            else:
                messages.append({"role": "user", "content":
                                 "Reply with one ```python block, or GUESS: <word>."})
            evict()
        if guess not in WORDS:
            messages.append({"role": "user", "content": f"{guess} is not in WORDS. Guess again."})
            evict()
            continue
        fb = feedback(guess, answer)          # independent check — harness, not model
        history.append((guess, fb))
        left = len(candidates(history))
        trace("B", "guess", guess_no=len(history), guess=guess, feedback=fb,
              left=left, tokens=tokens, repl_runs=repl_runs)
        if verbose:
            print(f"    B guess {len(history)}: {guess} -> {fb}   ({left} candidates remain, {repl_runs} REPL runs)")
        if fb == "GGGGG":
            return {"solved": True, "guesses": len(history), "tokens": tokens,
                    "repl_runs": repl_runs, "history": history}
        messages.append({"role": "user", "content": f"Feedback for {guess}: {fb}. Analyze or guess."})
        evict()
    return {"solved": False, "guesses": None, "tokens": tokens,
            "repl_runs": repl_runs, "history": history}


# --- the A/B ---

def report_run(label: str, r: dict):
    status = f"solved in {r['guesses']}" if r["solved"] else "FAILED (6/6 used)"
    extra = f"  repl_runs={r['repl_runs']}" if "repl_runs" in r else ""
    print(f"  {label}: {status}   rhae-style score {rhae_style(r['guesses']):.3f}   "
          f"tokens {r['tokens']}{extra}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--answer", type=str, default=None, help="fix the secret word")
    ap.add_argument("--selftest", action="store_true", help="offline mechanics test, no API")
    ap.add_argument("--json", type=str, default=None,
                    help="write the full per-turn trace and tally to this path")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    key = deepseek_key()
    if not key:
        sys.exit("Set DEEPSEEK_API_KEY (or legacy DEEPSEEK_API_PATAPI)")
    rng = random.Random(args.seed)

    a_wins = b_wins = 0
    a_scores, b_scores = [], []
    rounds = []
    global TRACE_ROUND
    for rnd in range(1, args.rounds + 1):
        TRACE_ROUND = rnd
        answer = args.answer.lower() if args.answer else rng.choice(WORDS)
        assert answer in WORDS, f"--answer must be one of the {len(WORDS)} embedded words"
        print("=" * 72)
        print(f"ROUND {rnd}/{args.rounds}   model={MODEL}   secret word withheld from both runs")
        print("=" * 72)
        print("  [A] naked model — plain chat, no tools")
        a = play_naked(key, answer)
        print("  [B] same model — code-writing harness (REPL + eviction + verification)")
        b = play_harnessed(key, answer)
        print(f"\n  answer was: {answer}")
        report_run("A naked    ", a)
        report_run("B harnessed", b)
        rounds.append({"round": rnd, "answer": answer,
                       "a": {k: v for k, v in a.items() if k != "history"},
                       "b": {k: v for k, v in b.items() if k != "history"}})
        a_scores.append(rhae_style(a["guesses"]))
        b_scores.append(rhae_style(b["guesses"]))
        ab = (a["guesses"] or 99, b["guesses"] or 99)
        if ab[1] < ab[0]:
            b_wins += 1
        elif ab[0] < ab[1]:
            a_wins += 1
        print()

    print("=" * 72)
    print(f"TALLY over {args.rounds} round(s):  harness better {b_wins}, naked better {a_wins}, "
          f"ties {args.rounds - a_wins - b_wins}")
    print(f"mean rhae-style score:  A naked {sum(a_scores)/len(a_scores):.3f}   "
          f"B harnessed {sum(b_scores)/len(b_scores):.3f}")
    print(f"(baseline = {HUMAN_BASELINE_GUESSES} guesses, a demo parameter — see docstring)")
    print("One round is an anecdote. Report the tally you actually got, including")
    print("any round the naked model wins.")
    print("=" * 72)

    if args.json:
        import datetime
        import json as _json
        os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
        with open(args.json, "w") as f:
            _json.dump({
                # NOT "rounds": that key carries the per-round list below, and a
                # dict literal with the same key twice keeps the last one silently.
                "model": MODEL, "seed": args.seed, "n_rounds": args.rounds,
                "max_tokens": MAX_TOKENS, "max_guesses": MAX_GUESSES,
                "words": len(WORDS), "baseline_guesses": HUMAN_BASELINE_GUESSES,
                "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "tally": {"harness_better": b_wins, "naked_better": a_wins,
                          "ties": args.rounds - a_wins - b_wins},
                "mean_rhae": {"a": sum(a_scores) / len(a_scores),
                              "b": sum(b_scores) / len(b_scores)},
                "tokens": {"a": sum(r["a"]["tokens"] for r in rounds),
                           "b": sum(r["b"]["tokens"] for r in rounds)},
                "solved": {"a": sum(1 for r in rounds if r["a"]["solved"]),
                           "b": sum(1 for r in rounds if r["b"]["solved"])},
                "rounds": rounds, "trace": TRACE,
            }, f, indent=1)
        print(f"wrote {args.json}  ({len(TRACE)} turn events)")
    return 0


# --- offline selftest (mechanics only, no API) ---

def selftest() -> int:
    assert len(WORDS) == len(set(WORDS)) and all(len(w) == 5 for w in WORDS), "word list broken"
    # feedback: exact, duplicate handling
    assert feedback("crane", "crane") == "GGGGG"
    assert feedback("speed", "erase") == "YBYYB"   # duplicate e: one G/Y max per available e
    assert feedback("allow", "world") == "BYBYY"  # first 'l' Y, second 'l' exhausted -> B
    assert feedback("aaaaa", "about") == "GBBBB"   # only one 'a' in answer -> one G, rest B
    # candidate filtering is consistent with feedback
    hist = [("crane", feedback("crane", "brand"))]
    cands = candidates(hist)
    assert "brand" in cands and "crane" not in cands
    assert all(feedback("crane", w) == hist[0][1] for w in cands)
    # rhae shape: solved-at-baseline = 1.0, 2x = 0.25 (capped), unsolved = 0
    assert rhae_style(4) == 1.0 and abs(rhae_style(8) - 0.25) < 1e-9 and rhae_style(None) == 0.0
    assert rhae_style(2) == 1.15  # cap
    # parsing
    assert parse_guess("I think... GUESS: crane") == "crane"
    assert parse_guess("no guess here") is None
    assert extract_code("```python\nprint(1)\n```") == "print(1)"
    print(f"selftest OK — {len(WORDS)} words, feedback/filter/rhae/parse all pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
