# Run logs — the evidence behind the numbers

Every claim the series makes about *what a demo did* comes from a run recorded here.
Claims taken from papers are a different thing and live in `../CLAIMS.csv`; the narrative
index of our own runs is `../RUNS.md`. **This folder is the raw material behind that
index** — the actual console output and the per-turn traces, unedited, including the parts
that went against us.

Linked from the video descriptions so you can check the work rather than take it.

---

## Why it is dated, and why the numbers move

Model ids in `demos/_config.py` and `demos/_llm.py` are **deliberately unpinned** — they
track whatever the current line is. That means these numbers are a snapshot, not a
constant, and re-running will not reproduce them exactly. That is not a caveat bolted on
afterwards; it is one of the series' actual findings. `wordle_ab.py` run twice on the same
seed, hours apart on the same day, disagreed about who won and about which side cost more.

**One claim survives every run of the A/B, and it is the only one the ad makes out loud:**
the model on its own can spend its entire completion budget reasoning and emit no guess,
and the same model inside a harness solved every round.

## How to reproduce

```bash
export DEEPSEEK_API_KEY=...          # the two DeepSeek demos
export OPENROUTER_API_KEY=...        # everything else

python3 demos/run_all.py --offline   # no keys needed; must pass
python3 demos/run_all.py             # the full suite
python3 demos/04_building/wordle_ab.py --rounds 5 --seed 42 --json out.json
```

Use a plain `python3` that has `requests` and `python-dotenv` — not a project virtualenv
built for something else. (Running the suite under this repo's *audio* venv fails three
demos on a missing `dotenv` and looks exactly like a broken demo. It isn't.)

## What is in each dated folder

| file | what it is |
|---|---|
| `run_all.log` | the whole suite, every demo, pass or fail, unedited |
| `wordle_ab.log` | the Episode 4 A/B, human-readable — every guess, every blank turn |
| `wordle_ab_verify.json` | that run's per-turn trace: guesses, feedback, candidates remaining, tokens, and the code the model wrote |
| `wordle_ab_ad_cut.json` | the specific run the ad's on-screen numbers are read from |
| `orchestrator.log`, `code_harness.log` | individual re-runs where the suite needed one |
| `ENVIRONMENT.txt` | interpreter, platform and model ids at the time |

The `.json` traces are what drives the ad's visuals — the tile colours, the counter, the
candidate counts and the quoted code are read from the file, not typed by hand, so what is
on screen cannot drift from what happened.
