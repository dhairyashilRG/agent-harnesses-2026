# AI Agent Harnesses — the companion repository

**AI Agent Harnesses** is a video series about the code *around* a language model: the
part that decides what it sees, what it can do, what it costs and whether it can be
trusted. A trailer, eight episodes and a bonus — about an hour and three-quarters in all.

The series' one-line thesis is a picture: **the model is an engine; the harness is the car
built around it.** An engine is magnificent, and on its own it goes nowhere.

This repository is everything the episodes promise you can check: the runnable demos, the
registry of every number spoken on camera, the evidence from our own runs, and the
scripts.

---

## Three promises, and how to check them

**Every number is primary-sourced.** Claims from papers and posts are in
[`CLAIMS.csv`](CLAIMS.csv), each with its source, its status and the date it was last
verified. Claims from our own runs are in [`RUNS.md`](RUNS.md), with the model, the date
and the command. If a number is on screen, it is in one of those two files — including the
ones still marked unverified.

**Every demo runs.** Plain Python, no framework, no mocks:

```bash
pip install -r demos/requirements.txt
python3 demos/run_all.py --offline    # no API key needed; this must pass
export OPENROUTER_API_KEY=sk-or-...   # one free key covers the live demos
python3 demos/run_all.py              # adds the live demos
```

Live demos are *skipped loudly* when there is no key, never silently passed. Model ids in
`demos/_config.py` are deliberately unpinned, so they track the current model line — which
means your numbers will differ from ours, and that is one of the series' findings.

**We hedge where the field hedges.** When a result is self-reported, the script says so.
When nobody has run the controlled experiment, it says "pattern, not proof". `RUNS.md`
records the same command, run three times in one day, telling three different stories.

---

## What is here

| | |
|---|---|
| [`demos/`](demos/) | The runnable demos, one folder per episode. Start with [`demos/README.md`](demos/README.md). |
| [`CLAIMS.csv`](CLAIMS.csv) | Every figure from a paper or post, with its primary source and verification date. |
| [`RUNS.md`](RUNS.md), [`runs/`](runs/) | Every figure from our own runs, and the raw logs behind them. |
| [`resources_2026.md`](resources_2026.md), [`REFERENCES.md`](REFERENCES.md) | The research behind the episodes, with the caveats each source carries. |
| [`sources/`](sources/) | The list of primary-source papers and where to fetch each one. |
| [`GLOSSARY.md`](GLOSSARY.md) | The terms, including ETCLOVG — the seven layers the series is built on. |
| [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) | Failures you will hit building a harness, and what fixes them. |
| [`scripts/`](scripts/) | The script of each episode, added as the episode is published. |

## The episodes

| | Episode | In one line |
|---|---|---|
| 0 | Trailer | What the series covers, and what it promises. |
| 1 | Foundations | How much of "the AI" is the model? |
| 2 | The Core Agent Loop | Four beats, and the model does one. |
| 3 | Anatomy of a Harness | Seven places a bug can live. |
| 4 | Building a Harness | The two hundred lines that do the work. |
| 5 | Advanced Patterns | More agents, and harnesses that rewrite themselves. |
| 6 | Evaluation | An agent scored 99% — what have you learned? |
| 7 | Production Realities | The failures that look like success. |
| 8 | Future Directions | Does any of this survive your next model? |
| 9 | Bonus: The Endpoint Lottery | You asked for a model by name. What do you actually get? |

## Corrections

If a number here is wrong, open an issue with the source. Corrections are dated and noted
in the episode's description rather than quietly fixed.

## Licence

Code is MIT — see [`LICENSE`](LICENSE). Papers cited here belong to their authors and are
linked, not redistributed.
