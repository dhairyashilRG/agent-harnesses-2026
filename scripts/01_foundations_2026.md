# Episode 1: Foundations — how much of "the AI" is the model?

**Duration: 11 min 2 s as published.**

> The dense concept opener that has to earn the series. Nothing structural changed in this
> rewrite; the language did, and the close now promises what the series actually delivers,
> including the non-transfer result in Episode 8. Every figure is in `CLAIMS.csv`.

---

## [0:00-0:30] COLD OPEN — the question

**Visual:** COMPARE — two bars, 52.8 and 66.5, "SAME MODEL (gpt-5.2-codex)" across both.

**Narrator:** "There is a thirteen-point gap between two versions of the same model, running
the same benchmark, on the same day. Nobody retrained anything. The only thing that changed
was the code wrapped around it."

**Narrator:** "That code has a name now. The harness. And the question this episode answers is
how much of what you call 'the AI' actually lives in it."

**Visual:** CARD — Title card: "AI Agent Harnesses — From Brain to Body."

---

## [0:30-2:40] THE ENGINE ON THE GROUND

**Visual:** SCENE — the engine alone on the workshop floor, running, going nowhere; then the
drivetrain, wheels and steering arrive around it as the narration names them.

**Narrator:** "Picture the most powerful engine ever built. Extraordinary on paper. Sitting on
the ground, it goes nowhere. It needs a transmission to move the power somewhere, wheels to
put it on the road, steering to point it, a frame to hold the whole thing together. That
complete system is what makes an engine useful."

**Visual:** REVEAL — three model names, each on its own plate, and under them what none of
them can do alone: stateless · isolated · can't touch anything.

**Narrator:** "Language models are in the same position. Claude Opus 5, GPT-6 Astra,
DeepSeek-V4, all genuinely extraordinary. On its own, a model is that engine on the floor.
Stateless, isolated, unable to touch anything."

**Visual:** COMPARE — the rank move, not the bars again: outside the top 30 → top 5, with
LangChain's own sentence under it.

**Narrator:** "The gap from the start of this episode is that analogy, measured. It comes from
LangChain, in February. Their DeepAgents system, on the Terminal Bench 2.0 coding benchmark,
moved from outside the top thirty into the top five, and nobody touched the model. Their
words: 'We only tweaked the harness and kept the model fixed.' That is a controlled experiment
rather than a slogan, and this series is about how they did it."

**Citation:** "Improving Deep Agents with Harness Engineering," langchain.com blog, 2026-02-17.

---

## [2:40-5:00] WHAT A MODEL CANNOT DO ALONE

**Visual:** COMPARE — split screen — what a model can do, against what it cannot do alone.

**Narrator:** "Be precise about what is missing, because 'models cannot do things' is too
vague to act on. A model is extraordinary at pattern matching, at reasoning over what is in
front of it, at producing text and code. What it cannot do is anything requiring it to last
outside itself."

**Visual:** REVEAL — each limitation appears as it is named, in its ETCLOVG layer colour.

**Narrator:** "It is stateless, so every conversation starts from nothing unless something
outside it remembers. It cannot touch the world. No files, no API calls, no running code, not
on its own. It sees only what fits in the window you handed it. Nothing carries from this
session to the next. And it does not learn from how any of it turned out."

**Visual:** REVEAL — the same list again, each item re-labelled as a job with an owner.

**Narrator:** "Now read that list a second way. Every one of those is a job. Remembering is a
job. Touching the world is a job. Deciding what stays in the window is a job. The harness is
the name for whoever does them, and for the rest of this series that is going to be you."

**Visual:** REVEAL — a three-line illustration, set as code but labelled as an
illustration rather than a file. It is the only non-runnable code frame in the series.

```python
# This is just an LLM call - stateless, isolated
response = llm.generate("What's the weather like?")
# It can't actually check weather - it just predicts text
```

**Narrator:** "And notice it is not lying when it says it cannot check the weather. It
genuinely cannot. There is no clock in there, no network, no yesterday. The prediction engine
is working perfectly. What is missing is a connection to the world, and in two episodes you
will be able to name exactly which layer that is."

---

## [5:00-7:40] HOW IT GOT A NAME

**Visual:** TIMELINE — the first stop only, 2020–21: prompt engineering, with zero-shot,
few-shot and chain-of-thought under it. The later years stay dim and unlabelled until the
narration reaches them, so no technique reads as belonging to a year it did not.

```
2020-2021: Prompt Engineering
2022: Agentic Prompting (ReAct)
2023: Context Engineering
2024: Harness Frameworks (LangGraph, AutoGen)
2025: Harness Engineering Formalization
2026: Named as a discipline; automated harness search
```

**Narrator:** "This did not arrive all at once. It started with prompt engineering, which was
the discovery that how you ask matters enormously. Zero-shot, few-shot, chain-of-thought. All
of it inside a single conversation."

**Visual:** TIMELINE — the 2022 row, with the ReAct loop drawing itself beside it.

**Narrator:** "Then ReAct, in 2022, which is the shift the next episode is about. The model
stopped only thinking and started emitting actions as well. Something outside ran those
actions and fed the results back. That is the modern agent pattern, and it is when models
could first use tools. Early systems were fragile. They lost track of what they were doing,
filled their context with junk, and fell over the first time a tool returned something
unexpected."

**Visual:** TIMELINE — the 2023 and 2024 rows.

**Narrator:** "Which made context management its own discipline in 2023. What do you keep,
what do you summarise, what do you go and fetch. Then frameworks arrived to package the whole
arrangement, and by 2025 survey papers had started treating it as a field with its own
patterns rather than a bag of tricks."

**Visual:** TIMELINE — the 2026 row, held.

**Narrator:** "And in February 2026 it got its name. OpenAI published a post calling it harness
engineering, which is where this series takes its title. By now there are harnesses that
search for better versions of themselves automatically, which is Episode five, and
code-centric harnesses where the action the model emits is executable Python, which is
Episodes two and eight."

**Narrator:** "The seven-layer taxonomy we use in Episode three comes from an OpenReview
preprint by Li and colleagues."

**Citation:** "Natural-Language Agent Harnesses," arXiv 2603.25723; "A Survey on Agent System
and Harness Design," arXiv 2606.20683. ETCLOVG: Li et al., **OpenReview preprint** — say
"preprint", never "TMLR" (`REFERENCES.md` §3). Meta-Harness, arXiv 2603.28052.

---

## [7:40-9:40] THREE WORDS, KEPT APART

**Visual:** REVEAL — three cards flipping to reveal definitions.

**Narrator:** "Three words get used interchangeably, and the whole series depends on keeping
them apart."

**Visual:** CARD — MODEL card.

**Narrator:** "The model is the thing you download or call. Text goes in, text comes out. That
is genuinely all it does, and it is worth being blunt about it, because most of what people
point at and call 'the AI' is not this part."

**Visual:** CARD — HARNESS card.

**Narrator:** "The harness is everything else. What tools exist and how they are described.
What stays in the context window and what gets thrown away. What happens when a step fails.
What gets logged, what gets checked, and what the thing is allowed to touch. It also covers
where code actually runs, and, as of this year, the machinery that lets a harness rewrite
itself."

**Visual:** CARD — AGENT card, then the equation MODEL + HARNESS = AGENT.

**Narrator:** "And an agent is those two things together, pointed at a goal. That is the whole
equation. So when somebody tells you their agent is better than yours, the useful question is
which half they changed."

**Visual:** COMPARE — two plates: the brain, held fixed; the body, rebuilt.

**Narrator:** "The model is the brain. The harness is the nervous system, the hands, the eyes
and the memory. The DeepAgents result at the start of this episode is what you get when you
hold the brain fixed and rebuild the body."

**Citation:** "Externalization in LLM Agents: A Unified Review," arXiv 2604.08224.

---

## [9:40-12:00] WHY THIS BECAME URGENT

**Visual:** REVEAL — four icons appearing — RELIABILITY, COST, DURATION, TOOLING.

**Narrator:** "People have been bolting tools onto models for years, so why did this become
urgent in the last eighteen months? Four things happened at once."

**Narrator:** "First, these went into production. Once an agent runs against real customers,
'it usually works' stops being acceptable. Consistency, failing gracefully, being debuggable
at three in the morning — every one of those lives in the harness, and none of them is
something you can prompt for."

**Visual:** NUMBER_LAND — the Codex figures landing one at a time: 5 months · ~1M lines · ~1,500 PRs ·
3 → 7 engineers · 3.5 PRs per engineer per day · about a tenth of the time.

**Narrator:** "Here is what that looks like at full scale. In February, OpenAI's Codex team
published a post about building an internal product of roughly a million lines over five
months. Application logic, tests, CI, docs, observability, internal tooling. In their words,
humans never directly contributed any code. About fifteen hundred pull requests, from a team
of three engineers that later grew to seven, and the throughput per engineer went *up* rather
than down. They estimate it took about a tenth of the time writing it by hand would have."

**Narrator:** "And the part worth stealing is what the humans actually did, which was
designing the environment, specifying intent, and building the feedback loops. That is a job
description changing while you watch."

**Citation:** "Harness engineering: leveraging Codex in an agent-first world,"
openai.com/index/harness-engineering, 2026-02-11.

**PRODUCTION NOTE:** Ryan Lopopolo is the author. **All figures verified in a browser
2026-09-09** — the page 403s to automated fetch. Verbatim table in `resources_2026.md` §1.3.
Keep the second citation card off screen; the first already carries the source.

**Visual:** COMPARE — cost comparison.

**Narrator:** "Second, cost stopped being a rounding error, and efficiency turned out to be a
harness property. In the Executable World Models paper we cover in Episode six, one
two-hundred-dollar-a-month subscription was enough to run their full experiments for, in their
words, roughly two to eight games. And Stanford's Meta-Harness found a harness that beat a
state-of-the-art context manager while using four times fewer context tokens."

**Visual:** DIAGRAM — a task duration bar stretching from one turn to six hours.

**Narrator:** "Third, the tasks got longer. A single question and answer needs almost no
harness. An agent working for six hours needs somebody deciding what it still remembers at
hour five, and that is an engineering problem rather than a prompting one."

**Visual:** REVEAL — framework cards.

**Narrator:** "And fourth, the tooling caught up. Frameworks now ship harness concerns as
named features. Vercel's AI SDK 7 has an experimental HarnessAgent that treats sandboxes,
permissions and context compaction as first-class parts of the harness. The patterns have
names now, which is what makes this teachable at all."

---

## [12:00-13:30] WHAT THIS SERIES IS, AND WHAT IT WILL NOT CLAIM

**Visual:** REVEAL — the episode roadmap appearing.

**Narrator:** "Over the next eight episodes we go from the core loop, to the seven layers of a
harness, to building one from scratch in about two hundred lines that runs live against a real
model. Then advanced patterns, including a harness that rewrites itself. Then how to measure
any of it without fooling yourself. Then production, where you meet the failures that run
green. And then the open question."

**Visual:** COMPARE — the counterweight card — Tufa's sentence on one side, the DeepAgents bars on the
other.

**Narrator:** "And I want to set the honest counterweight up now, because the series carries it
all the way through. Tufa Labs, who built a winning harness, say the model decides what is
*solvable* and the harness mostly decides what it *costs*. The DeepAgents result says the
harness moved solve rate with the model held fixed. Both are primary sources. Both are true.
Where the line sits between them is genuinely open, and Episode eight is where we put the two
side by side."

**Visual:** CARD — the Episode 8 teaser card, dim: "the harness you build will not transfer".

**Narrator:** "One more thing I will promise you, because it is the most useful finding in the
series and it arrives last. The published work this year, and a small reproduction of our own,
both say that a harness tuned for one model does not carry over to the next one. Which changes
what is worth learning here. The settings will not survive your next model. The anatomy and the
habit of measuring will."

---

## [13:30-15:00] CLOSE

**## HARNESS IN THE WILD — OpenAI Codex.**

What the humans built was not the code. It was the environment and the feedback loops. Steal
the framing rather than the scale: when your agent struggles, the question is never how to
prompt it better. It is what capability is missing, and how you make that capability legible
and enforceable.

**## KEY TAKEAWAYS (slide — hold 5s):**
- **The harness is the code around the model** that decides what it stores, retrieves and sees.
- **Same model, better harness: +13.7 points** on a real benchmark, model held fixed.
- **2026 is when this got a name** and a discipline.
- **The counterweight:** the model sets what is solvable, the harness sets what it costs. The
  boundary is the open question of the series.
- **The humans' job moved** from writing code to designing feedback loops.

**## RECAP**

A model alone is an engine on the ground. Stateless, isolated, unable to touch anything. The
harness is everything that makes it act, and in 2026 that got a name, a controlled result with
the model held fixed, and a proof at scale in OpenAI's own codebase. It also comes with a
tension we carry all series: does the harness move capability, or only cost?

**## TRY THIS YOURSELF**

Run `demos/01_foundations/simple_llm_call.py` and ask it for the weather. Watch it tell you,
perfectly honestly, that it has no way to find out. That is the engine on the ground. Then run
`demos/01_foundations/minimal_harness.py`. Same model, same question, except now it calls a
real weather API, gets a real temperature, and chains a second tool to convert it to
Fahrenheit. Nothing about the model changed. Eighty lines around it changed. That gap is the
whole series in two files, and both run on one free API key.

**Visual:** CARD — Final title card: "Next — The Core Agent Loop."

**Narrator:** "Next time, the four-beat loop under almost every agent ever built, and the one
beat of it the model actually does."

---

## Production Notes for Episode 1

**Visual assets:** the engine-on-the-ground and assembled-car 3D shots; the timeline; the
DeepAgents two-bar chart, which recurs in Episodes 6, 7 and 8 and should be built once; the
three definition cards; the four-forces icons; the Codex figure reveal. **New build:** the dim
Episode 8 teaser card for the non-transfer promise.

**Runnable code:** `demos/01_foundations/simple_llm_call.py` and `minimal_harness.py`. Verified
2026-09-10 — declines without tools; with tools, live 23.0°C chained to 73.4°F. Re-run on the
day; the temperature will differ and that is the point.

**Say-it-exactly list:** "experimental" (AI SDK 7 HarnessAgent); "preprint", never "TMLR"
(ETCLOVG); "model held fixed" (DeepAgents); "roughly two to eight games" (EWM, verbatim).

**Cut for cause:** the old close ran "not just the what, but the why; not just the theory, but
the practice; not just what works in 2024, but 2026" — three negative contrasts in a row that
promise nothing checkable. The roadmap beat replaced it and names what each episode contains.

**Sources:** langchain.com blog 2026-02-17 · openai.com/index/harness-engineering 2026-02-11 ·
arXiv 2603.25723 · arXiv 2606.20683 · arXiv 2604.08224 · arXiv 2603.28052 · arXiv 2605.05138.
