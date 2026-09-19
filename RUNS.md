# Run provenance — every narration claim that came from executing something

`CLAIMS.csv` tracks claims sourced from **papers**. This file tracks claims sourced from
**our own runs**, which is a different kind of fragile: a paper's number doesn't change
when you re-read it, and a live model's does.

Any narration that asserts what a demo *did* — a score, a token count, a behaviour —
belongs here with the date and model that produced it. If a claim isn't in this table, it
should not be stated on camera as a result.

**Re-run everything below on recording day.** Model IDs move (`demos/_config.py` uses
unpinned defaults on purpose, so they track the current line), and the numbers move with
them.

---

## Verified runs

| Claim | Demo | Model | Date | Result | Stability |
|---|---|---|---|---|---|
| Baseline solves every task, `mine()` returns `None`, A/B never fires (Ep 5) | `05_advanced/self_improving_harness.py` | `deepseek-flash` | 2026-09-10 | **4/4 solved, 0 REPL errors, no lesson mined** | **3 runs of 3** — stable |
| Offline suite passes with no API key | `demos/run_all.py --offline` | — | 2026-09-10 | 7 passed, 0 failed | deterministic |
| Model alone cannot answer "weather in SF"; with tools it can (Ep 1) | `01_foundations/simple_llm_call.py` + `minimal_harness.py` | `meta/muse-glimmer-30b` | 2026-09-10 | declines without tools; **with tools: live 23.0°C, chained `calculate` -> 73.4°F** | shape stable |
| ReAct loop chains two tool calls and finishes (Ep 2) | `02_core_loop/react_agent.py` | `meta/muse-spark-1.3` (the `demos/_llm.py` default) | 2026-09-11 | 3 steps, 2 calculator calls, 445. The run filmed in shot s12: 3717 tokens, 14.5 s | shape stable; step and call counts repeat, token and latency totals do not |
| Orchestrator decomposes, assigns, synthesizes (Ep 5) | `05_advanced/orchestrator.py` | `meta/muse-glimmer-30b` | 2026-09-10 | 4 subtasks across 3 workers, synthesized | shape stable |
| Generate -> test -> refine produces passing code (Ep 8) | `08_future/code_harness.py` | `meta/muse-glimmer-30b` | 2026-09-10 | 2/2 tests pass | shape stable |
| Flagship harness solves the task and the independent check agrees (Ep 4) | `04_building/duck_harness_simplified.py` | `deepseek-flash` | 2026-09-12 | **answer 816, ground truth 816, correct YES; 1 REPL execution, 2 turns, 354 prompt + 152 completion** | shape stable; **token counts are not** |

## The Ep 4 A/B — the series thesis, measured

`04_building/wordle_ab.py --rounds 5 --seed 42`, `deepseek-flash`, **2026-09-12**. Same
model both sides; the secret word is withheld from both.

| | A — naked model | B — same model + harness |
|---|---|---|
| Rounds won | **0** | **4** (1 tie) |
| Solved | **1 of 5** | **5 of 5** |
| Mean RHAE-style score | **0.230** | **1.120** |
| Tokens across the five | **70,241** | **47,027** |

Per round: `route` 2/2 tie · `board` failed/3 · `ahead` failed/2 · `stand` failed/2 ·
`enemy` failed/4.

**The naked model's failure mode is not bad guessing.** In three of the five rounds it
never produced a guess at all: it spent **15,999 of its 16,000 completion tokens
reasoning** and emitted nothing. A blank turn, at full price. Deducing a word from three
colour patterns is exactly the kind of search that runs away in tokens; the harnessed run
does not do it, because it writes four lines of Python that filter a list instead.

**Read the tally, not a round.** The same morning, `--rounds 1 --seed 7` went the other
way — the naked model solved in two and the harness took three. On 2026-09-10 that same
seed had the naked run fail outright and the harness spend 60% *more* tokens than it. Three
different stories from the same script in three days. The distribution is the claim.

**The rig used to hide this.** A naked turn that exhausted its completion budget raised out
of `call_model` and aborted the whole comparison, so the only multi-round tallies that ever
finished were the ones where the naked model happened to survive. It now records a
budget-exhausted turn as the failed turn it is (`BudgetExhausted`, 2026-09-12). A measuring
rig that aborts on a bad result only ever reports good ones.

## The same command, twice in one day — the run the ad cut is built on

`04_building/wordle_ab.py --rounds 5 --seed 42 --json run.json`,
`deepseek-flash`, **2026-09-12 07:14 UTC**. The seed fixes the words, so this is the same
five puzzles as the run above — `route`, `board`, `ahead`, `stand`, `enemy` — played by
the same model from the same prompts, hours apart.

| | A — naked | B — + harness | the run above, same day |
|---|---|---|---|
| Solved | **2 of 5** | **5 of 5** | 1 of 5 / 5 of 5 |
| Rounds won | **1** | **3** (1 tie) | 0 / 4 (1 tie) |
| Tokens | **27,667** | **49,898** | 70,241 / 47,027 |
| Mean RHAE-style | 0.460 | 1.150 | 0.230 / 1.120 |

Two things this run says that the earlier one did not, and the ad cut states both on
screen rather than choosing the flattering half:

**The harness cost 80% more, not a third less.** Same task, same model, opposite sign on
the cost axis. Only one claim survives both runs: the harness solved 5 of 5 in each. That
is the claim — reliability. Savings is not, and the ad does not say it is.

**The naked model won a round.** It also solved two, up from one. "Usually, not always" is
what this demo supports; a tally that never moves is a tally nobody re-ran.

**The blank turn is still there, and it is worse than reported.** Round 3: after `audio`
came back `GBYBB` the field was down to **three words**, and the model then spent
**16,000 of 16,000 completion tokens — every one of them reasoning — and emitted
nothing.** It failed from a winning position, which is the failure worth filming.

**What the harness actually wrote is not four lines.** Every REPL turn in this run was
between **10 and 48 lines**; in round 3 it wrote a 24-line entropy solver that scored
every candidate by how much a guess would narrow the field, and played the top of its own
list. The earlier "four lines of Python" gloss was true of an older run and is not true of
this one — `demos/04_building/wordle_ab.py --json` now records the code so the claim can
be checked instead of remembered.

---

## Three runs of one command, one day — what actually survives

`wordle_ab.py --rounds 5 --seed 42`, `deepseek-flash`, all on **2026-09-12**. The seed
fixes the words, so all three played the same five puzzles from the same prompts. Raw logs
and per-turn traces: `runs/2026-09-12/`.

| | run 1 | run 2 (07:14) — the ad | run 3 (16:37) — verification |
|---|---|---|---|
| Naked solved | 1 of 5 | 2 of 5 | **4 of 5** |
| Harness solved | **5 of 5** | **5 of 5** | **5 of 5** |
| Rounds won (naked–harness) | 0–4 | 1–3 | 0–1 (4 ties) |
| Tokens, naked | 70,241 | 27,667 | 56,439 |
| Tokens, harness | 47,027 | 49,898 | 54,290 |

**Almost nothing is stable.** The naked model solved one, then two, then four. The harness
cost 33% less, then 80% more, then 4% less. Anyone reporting a single run of this could
honestly tell three different stories, and two of them would be wrong.

**Two things held across all three, and they are the only two the ad says out loud:**

1. **The harness solved 5 of 5. Three times out of three.** Reliability is the claim —
   not speed, not savings.
2. **The naked model can spend its whole budget and produce nothing.** Run 3 had two such
   turns, at **16,000** and **15,999** of 16,000 completion tokens, every one of them
   reasoning. The ad's number is reproduced exactly.

This is what the discipline is for. The ad was written to claim only what survives every
run, and a third run — where the naked model performed far better than in either of the
others — did not cost it a single word.

---

## The token-count warning

Three identical runs of the Ep 5 demo on 2026-09-10 produced:

| Run | Solved | REPL errors | Avg turns | Completion tokens |
|---|---|---|---|---|
| 1 | 4/4 | 0 | 1.00 | **933** |
| 2 | 4/4 | 0 | 1.50 | **4,350** |
| 3 | 4/4 | 0 | 1.50 | **4,836** |

The Ep 4 flagship moved the same way: **313 + 132** tokens on 2026-07-17, **354 + 264** on
2026-09-10, **354 + 152** on 2026-09-12 — while the run's *shape* (one REPL execution, two
turns, answer 816, independent check agrees) was identical every time.

**Correctness was identical; cost varied 5×.** Same tasks, same model, same prompt, minutes
apart. The agent sometimes solved a task in one turn and sometimes took two, and each extra
turn re-sends the whole conversation.

Two consequences:

1. **Never state a token count as a property of the harness.** Ep 4's figures are only
   defensible because they are spoken as *"on our 2026-09-10 run."* Keep that framing, and
   re-run for a fresh number before recording — the July numbers were already wrong by then.
2. **The variance is itself the lesson**, and better material than the number. If cost swings
   5× while the answer stays the same, then "what does this agent cost" has no single answer
   — which is exactly why Episode 6 treats efficiency as a distribution and why RHAE squares
   the action penalty. Consider using the three-run table on screen in Ep 4's COST & TOKENS
   beat instead of a single figure.

## Two OpenRouter account gates (both hit, both real)

1. **18+ attestation.** The whole Muse Spark family returns 403 with
   `missing_attestation_types: ["age_18plus"]` until confirmed at
   <https://openrouter.ai/settings/preferences>. Cleared 2026-09-10.
2. **Paid-endpoint training.** `meta/muse-spark-1.3-contributor` *additionally* returns 404
   — `"Paid model training violation (account settings)"` — unless the account allows paid
   endpoints that train on inputs. That is what the "contributor" tier *is*: about a third
   of the price, paid for with your prompts.

**The default is `meta/muse-spark-1.3`** (non-contributor), which serves once gate 1 is
cleared. A public repo's default should not quietly opt a stranger into having their
prompts trained on; set `OPENROUTER_MODEL` for the cheaper tier on your own runs.

## Tooling comparison — the Ep 3 beat (2026-09-10)

Same question ("today's date and the current weather in San Francisco"), same model
(`meta/muse-glimmer-30b`), three tool configurations:

| Configuration | Answer | Cost |
|---|---|---|
| No tools | correct date, **declines** on weather | $0.0002 |
| `:online` web search | weather + citation, but dated **September 4** — six days stale | **$0.0083** |
| Purpose-built `get_weather` | `23.0°C, humidity 48%, local time 2026-09-10T09:30` | ~$0.0002 |

The broad tool was ~40× the cost, less accurate, and *more* persuasive because of the
citation. One run of a live system — re-check before quoting "six days" on camera.

## How to re-verify

```bash
export OPENROUTER_API_KEY=sk-or-...
export DEEPSEEK_API_PATAPI=...      # or DEEPSEEK_API_KEY
python3 demos/run_all.py --offline  # must pass with no keys at all
python3 demos/run_all.py            # the 8 live demos
python3 demos/05_advanced/self_improving_harness.py   # the Ep 5 claim specifically
```

Then update the table above with the date, the model id, and what actually happened —
including if it disagrees with what's written in a script. A script that disagrees with a
run is a script bug, not a run bug.

## Endpoint measurements (2026-09-12 and -13) — Episodes 6, 8 and 9

These are readings of a public API rather than experiments, so anyone can check them in a
minute. All through OpenRouter.

| Claim | How to re-verify |
|---|---|
| One open-weight model id was served by **28 endpoints** spanning fp4, fp8 and bf16, priced **$0.03 to $0.44** per million input tokens on 2026-09-12 | `GET /api/v1/models/<id>/endpoints` |
| **4 of 12** endpoints for `minimax/minimax-m3` cannot call tools at all; pinning one returns a 404 whose routing funnel reads `Initial 12 → Tool Compatibility 8 → Fallback 0` | the same endpoint list, check `supported_parameters` |

**Captured 2026-09-13.** The four endpoints that do not declare `tools` were
`coreweave/fp4`, `gmicloud/fp8`, `streamlake/fp8` and `sambanova`. Pinning `coreweave/fp4`
with `allow_fallbacks: false` and a tool in the request returned the 404 and the
three-step funnel. The raw response is in `runs/2026-09-13_routing_funnel/`, with the
account id removed. Endpoint lists and prices move; check the date before you quote them.

The controlled precision study behind Episode 9 (240 trials) is published alongside that
episode.

## Claims that are safe without a run

These are structural and verifiable by reading the code, so they don't need re-running:

- What each function does (`_evict` keeps the system prompt plus the last N messages;
  `mine()` returns `None` when no trace failed; `REPL.run` uses a subprocess with a timeout).
- That every identifier shown on screen exists in `demos/` — checked mechanically across all
  nine scripts on 2026-09-09.
- Anything sourced from a paper — that lives in `CLAIMS.csv`.

