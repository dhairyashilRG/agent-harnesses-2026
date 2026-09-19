# AI Agent Harness — Code Demos

Working examples for the video series, one folder per episode.

## Layout (actual files)

```
demos/
├── SAFE_CALCULATOR.py          # Safe AST math (no eval)
├── 01_foundations/
│   ├── simple_llm_call.py      # Stateless LLM call
│   └── minimal_harness.py      # Minimal ReAct loop
├── 02_core_loop/
│   ├── react_agent.py
│   └── trace_viz.py
├── 03_anatomy/
│   └── code_as_harness.py
├── 04_building/
│   ├── duck_harness_simplified.py   # Live DeepSeek + REPL (flagship Ep 4)
│   ├── wordle_ab.py                 # Same model, two harnesses — Wordle A/B (Ep 4 money shot)
│   └── secure_harness.py            # Secure tool path (no eval)
├── 05_advanced/
│   ├── orchestrator.py
│   └── self_improving_harness.py    # Meta-Harness miniature (DeepSeek)
├── 06_evaluation/
│   ├── arc_agi3_runner.py           # RHAE-style scoring demo
│   └── evaluator.py
├── 07_production/
│   └── logger.py
└── 08_future/
    └── code_harness.py
```

## Setup

```bash
# Deps (exactly what the demos import — see requirements.txt)
pip install -r requirements.txt   # requests, python-dotenv

# Most demos: one OpenRouter key, any of its models
export OPENROUTER_API_KEY=sk-or-...          # https://openrouter.ai/keys
# optional: export OPENROUTER_MODEL=<model id>   (default: meta/muse-spark-1.3)

# Three demos call DeepSeek directly
export DEEPSEEK_API_KEY=your_key             # legacy DEEPSEEK_API_PATAPI still works
```

**API split (current):**

| Demo | Provider |
|------|----------|
| `01`–`03`, `orchestrator`, `code_harness` | OpenRouter, via `demos/_llm.py` |
| `duck_harness_simplified.py`, `wordle_ab.py`, `self_improving_harness.py` | DeepSeek (`deepseek-flash`) |

Every model call in the first group goes through **`demos/_llm.py`**, one provider boundary
for the whole repo — switching model is one env var, and the harness around it never
notices. That is the Episode 3 point made concrete. The three DeepSeek demos deliberately
call that API directly, so you can see the raw wire format at least once.

**Two OpenRouter account settings can block a model** and the error is easy to misread:
some models need a one-time 18+ confirmation, and any `-contributor` tier additionally
needs "allow paid endpoints that train on inputs" — that discount is paid for with your
prompts. Both are at <https://openrouter.ai/settings>. See `RUNS.md`.

`wordle_ab.py` extras: `--rounds N --seed N` for a repeated A/B, `--answer WORD` to fix the
secret, `--selftest` for the offline mechanics test (no key needed — part of `run_all.py`'s
offline suite).

## Run

```bash
python 01_foundations/simple_llm_call.py
python 04_building/duck_harness_simplified.py
python 05_advanced/self_improving_harness.py
python 06_evaluation/arc_agi3_runner.py
```

## Notes

- Prefer **`secure_harness.py`** / **`SAFE_CALCULATOR.py`** over any code that uses `eval()`.
- `minimal_harness.py` and `react_agent.py` still contain `eval()` for a calculator tool — do not present them as production-safe.
- Re-run live-API demos on recording day; they print real token counts and answers.
- `self_improving_harness.py` may score a perfect baseline (nothing to mine) — that is an honest teaching result (see Ep 5 plan).
