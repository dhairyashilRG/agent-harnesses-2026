# Episode 0: Trailer / Roadmap (2026)

**Duration: 3 min 19 s as published.**

> Leads with the DeepAgents result, states the thesis and its honest counterweight, then the
> roadmap, prerequisites and repo link. Pin as Episode 0 and paste the roadmap in a pinned
> comment. Every number is in `CLAIMS.csv`. **Re-checked 2026-09-13** against the rewritten
> episodes, so the promises here match what the series actually delivers.

---

## [0:00-0:50] COLD OPEN — same model, +13.7 points

**Visual:** COMPARE — two bars, 52.8 → 66.5 on Terminal Bench 2.0, "SAME MODEL (gpt-5.2-codex)" across
both in large type. Rank overlay: Top 30 → Top 5.

**Narrator:** "In February, LangChain took a coding agent from fifty-two-point-eight to
sixty-six-point-five on a real benchmark, from outside the top thirty into the top five, and
they did not touch the model. Their words: 'We only tweaked the harness and kept the model
fixed.'"

**Narrator:** "Thirteen-point-seven points, from the code around the model. That code has a
name now. It is called the harness, and it is where a great deal of what you think of as 'the
AI' actually lives. This series is about building one."

**Visual:** CARD — Title card: "AI Agent Harnesses — 2026."

**Citation:** langchain.com DeepAgents post, 2026-02-17.

---

## [0:50-1:50] THE THESIS, AND WHAT CUTS AGAINST IT

**Visual:** COMPARE — the thesis on one card: *"The harness is where reliability and cost are won or
lost."* Then a second card arrives beside it with Tufa's quote.

**Narrator:** "The thesis of the series is that the harness — the code deciding what the model
stores, retrieves and sees — is where reliability and cost are won or lost. And I am going to
give you the thing that cuts against it in the same breath, because a series about honest
measurement should not open by hiding its counterevidence."

**Narrator:** "Tufa Labs built the harness that won ARC Prize Milestone One. They say, quote,
'solvability of a game being dependent on model capability, while the cost is mostly dictated
by the harness.' The model decides what is possible. The harness decides what it costs. And
yet DeepAgents moved solve rate by thirteen-point-seven points with the model held fixed. Both
are primary sources. They cannot both be the whole truth, and where that boundary sits runs
through every episode."

**Citation:** tufalabs.ai/research/duck-harness.

---

## [1:50-3:10] THE ROADMAP

**Visual:** REVEAL — episode list, each with its one-line anchor.

**Narrator:** "Here is where we are going."

- **Episode 1 — Foundations.** How much of "the AI" is the model, and the month in 2026 the
  harness got its name.
- **Episode 2 — The Core Loop.** Think, act, observe. Four beats, and the model does one of
  them.
- **Episode 3 — Anatomy.** Seven layers, seven places a bug can live. Our colour system for
  the rest of the series.
- **Episode 4 — Building one.** About two hundred lines, live against a real model, plus a
  Wordle A/B where the same model wins and loses depending on what is wrapped around it.
- **Episode 5 — Advanced patterns.** More agents, and a harness that rewrites itself.
- **Episode 6 — Evaluation.** Somebody tells you an agent scored ninety-nine percent. Four
  questions before that means anything.
- **Episode 7 — Production.** The failures that run green: the empty reply, the verifier that
  passed a transposition, the endpoint you did not pin.
- **Episode 8 — Does any of this survive your next model?** Harness gains are real and they do
  not transfer. What you keep, and what you re-measure.
- **Episode 9 — The endpoint lottery.** A bonus episode on what you actually get when you ask
  for a model by name, and why some of those things cannot run an agent at all.
- **Plus Office Hours**, a bonus question-and-answer episode.

---

## [3:10-4:10] THREE PROMISES, AND WHAT YOU NEED

**Visual:** REVEAL — three promises on screen.

**Narrator:** "Three promises. First, every number is primary-sourced. No anonymous
benchmarks and no 'Company X cut costs forty percent' stories. The real cases are better and
they are all cited, with the papers archived in the repo."

**Narrator:** "Second, every demo runs. Real API calls, real tokens on screen, and real
failures we do not edit out, including a live bug where the model returns two hundred OK and
an empty string."

**Narrator:** "Third, we report what survives re-running. When we ran our headline comparison
three times in one day it told three different stories, so the series says the two things that
held all three times and nothing else. When a figure is self-reported, we say so. When nobody
has run the experiment, we say pattern rather than proof."

**Visual:** CARD — prerequisites card.

**Narrator:** "What you need is Python, an API key, and having called a language model at least
once. If you can run a Python file, you can build along."

---

## [4:10-4:50] CLOSE

**Visual:** REVEAL — repo link, large. The `demos/` tree and `sources/` archive flash by.

**Narrator:** "Everything is in the repo linked below. Every script, every runnable demo, the
primary-source archive, and a claims register so you can check our work against it. Clone it
and build each harness alongside me. By Episode four you will have a working code-writing
agent. By Episode eight you will know which parts of it are worth keeping when you change
models. And there is a bonus episode after that on the thing none of the disclosure standards
ask about."

**Visual:** CARD — Final card → auto-roll into Episode 1.

---

## Production Notes for Episode 0 (2026)

**Pin as Episode 0.** Paste the Episode 1–9 list into a pinned comment.

**Visual assets:** the two-bar DeepAgents chart (V2 — the cold open, and the single most
persuasive image in the series; do not overbuild it), the thesis-and-counterweight two-card,
the roadmap, the three-promises card.

**Say-it-exactly list:** "We only tweaked the harness and kept the model fixed" (verbatim,
DeepAgents); "solvability… dependent on model capability, while the cost is mostly dictated by
the harness" (verbatim, Tufa); "primary-sourced"; "every demo runs"; "pattern, not proof".

**Keep it tight.** Lead with the number, land the tension, show the roadmap, point at the
repo. Teach nothing; that is Episode 1.

