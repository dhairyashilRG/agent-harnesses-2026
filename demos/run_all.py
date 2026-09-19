#!/usr/bin/env python3
"""
Smoke-test runner for the demo suite.

This is the automated version of the pre-recording checklist item "re-run all demos on
the day." It classifies each demo as OFFLINE (no network/API — must pass) or LIVE (hits a
real API — runs only if the key is set, otherwise SKIPPED, never a silent pass).

    python3 demos/run_all.py            # run everything available
    python3 demos/run_all.py --offline  # offline demos only (CI-safe, no keys)

Exit code is nonzero if any demo that RAN failed. Skipped live demos do not fail the run,
but they are reported loudly so "all green" never hides an unexercised path.
"""

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (path [+ args], kind, required_env)  kind in {"offline", "live"}
DEMOS = [
    ("06_evaluation/arc_agi3_runner.py", "offline", None),
    ("06_evaluation/evaluator.py",       "offline", None),
    ("07_production/logger.py",           "offline", None),
    ("02_core_loop/trace_viz.py",         "offline", None),
    ("03_anatomy/code_as_harness.py",     "offline", None),
    ("SAFE_CALCULATOR.py",                "offline", None),
    ("04_building/wordle_ab.py --selftest", "offline", None),
    ("01_foundations/simple_llm_call.py", "live", "OPENROUTER_API_KEY"),
    ("01_foundations/minimal_harness.py", "live", "OPENROUTER_API_KEY"),
    ("02_core_loop/react_agent.py",       "live", "OPENROUTER_API_KEY"),
    ("05_advanced/orchestrator.py",       "live", "OPENROUTER_API_KEY"),
    ("08_future/code_harness.py",         "live", "OPENROUTER_API_KEY"),
    ("04_building/duck_harness_simplified.py", "live", "DEEPSEEK_API_KEY|DEEPSEEK_API_PATAPI"),
    ("04_building/wordle_ab.py",               "live", "DEEPSEEK_API_KEY|DEEPSEEK_API_PATAPI"),
    ("05_advanced/self_improving_harness.py",  "live", "DEEPSEEK_API_KEY|DEEPSEEK_API_PATAPI"),
]


def has_key(spec):
    if not spec:
        return True
    return any(os.getenv(name) for name in spec.split("|"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="run only offline demos")
    args = ap.parse_args()

    passed, failed, skipped = [], [], []
    for path, kind, env in DEMOS:
        if args.offline and kind == "live":
            continue
        if kind == "live" and not has_key(env):
            skipped.append((path, f"missing {env}"))
            print(f"SKIP  {path}  ({env} not set)")
            continue
        print(f"RUN   {path} ...", flush=True)
        parts = path.split()  # "file.py --flag" -> script + args
        cmd = [sys.executable, os.path.join(HERE, parts[0])] + parts[1:]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode == 0:
            passed.append(path)
            print(f"PASS  {path}")
        else:
            failed.append(path)
            tail = (r.stderr or r.stdout).strip().splitlines()[-3:]
            print(f"FAIL  {path}\n      " + "\n      ".join(tail))

    print("\n" + "=" * 60)
    print(f"passed {len(passed)}   failed {len(failed)}   skipped {len(skipped)}")
    if skipped:
        print("skipped (set the key to exercise these on camera):")
        for p, why in skipped:
            print(f"  - {p}  [{why}]")
    print("=" * 60)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
