# Resources — AI Agent Harness Series (verified July 2026)

Every link and number below was checked against a **primary source** on 2026-07-17.
Anything not verifiable is marked UNVERIFIED and must not be stated as fact on camera.

---

## 1. The three pillars (all verified, all primary)

These are the spine of the series. Each is a real, citable case of the harness —
not the model — moving the number.

### 1.1 LangChain DeepAgents — the controlled experiment

- Source: https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering
- Published **February 17, 2026** (LangChain's own blog — primary)

| Fact | Value |
|---|---|
| Benchmark | Terminal Bench 2.0 |
| Before | **52.8** |
| After | **66.5** |
| Gain | **+13.7 points** |
| Rank | **Top 30 → Top 5** |
| Model | **gpt-5.2-codex, held fixed** |

Verbatim: *"We only tweaked the harness and kept the model fixed."*

The three levers they moved:
1. **System prompt** — a build-verify loop (plan → implement with tests in mind →
   verify → fix).
2. **Middleware** — `PreCompletionChecklistMiddleware` (self-verification) and
   `LoopDetectionMiddleware` (catches doom loops via file-edit tracking).
3. **Context injection** — `LocalContextMiddleware` maps directories and discovers
   tools; plus time-budget warnings.

They used LangSmith tracing at scale to find failure modes, then fixed the harness.

**Caveat for camera:** the post does **not** attribute gains to individual changes.
It says *"self-verification & tracing help a lot."* Don't break the 13.7 into parts.

**This is the cleanest "harness leverage" citation in the series.** Same model, same
benchmark, only the harness changed. Use it as the anchor.

### 1.2 Meta-Harness — automating the harness itself

- Paper: https://arxiv.org/abs/2603.28052
- Code: https://github.com/stanford-iris-lab/meta-harness
- **"Meta-Harness: End-to-End Optimization of Model Harnesses"**
- Authors: Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab,
  Chelsea Finn (Stanford / MIT / KRAFTON)
- Submitted **March 30, 2026**

Verbatim from the abstract:

> "The performance of large language model (LLM) systems depends not only on model
> weights, but also on their harness: the code that determines what information to
> store, retrieve, and present to the model. Yet harnesses are still designed largely
> by hand, and existing text optimizers are poorly matched to this setting because
> they compress feedback too aggressively."

Results, verbatim:
- Online text classification: **improves over a state-of-the-art context management
  system by 7.7 points while using 4x fewer context tokens.**
- Retrieval-augmented math: **a single discovered harness improves accuracy on 200
  IMO-level problems by 4.7 points on average across five held-out models.**
- Agentic coding: **discovered harnesses surpass the best hand-engineered baselines
  on TerminalBench-2.**

Mechanism: an **agentic proposer** that reads the source code, scores, and execution
traces of all prior candidates **through a filesystem**. The paper's own framing of
why this works: *"richer access to prior experience can enable automated harness
engineering"* — existing text optimizers fail because they **compress feedback too
aggressively**.

Note the through-line: Meta-Harness beats hand-engineered baselines on
**TerminalBench-2** — the same benchmark family DeepAgents hand-tuned in §1.1
(**Terminal Bench 2.0**). Automated search is now competitive with expert
hand-engineering on the same task.

> **Spelling caveat (flagged 2026-07-18):** the Meta-Harness paper writes
> *"TerminalBench-2"*; the LangChain post writes *"Terminal Bench 2.0."* These are
> almost certainly the same benchmark (Terminal-Bench, version 2), and the series treats
> them as such — but no source states the equivalence outright. If you make the
> "same benchmark" point on camera, either confirm it (tbench.ai) or say "the same
> Terminal-Bench 2 family." Tracked in `CLAIMS.csv`.

### 1.3 OpenAI Codex — harness engineering named as a discipline

- Source: https://openai.com/index/harness-engineering/
- Secondary: https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/
- Published **February 11, 2026**

An internal **beta product** shipped with **no manually written source code** —
~**1M lines of code**. Application logic, tests, CI, docs, observability, and internal
tooling were Codex-written; humans focused on **designing environments, specifying
intent, and providing structured feedback** (prompts, PR review, CI workflows) rather
than implementing code.

**Verification status: VERIFIED 2026-09-09** — the primary post was opened in a real
browser (it returns HTTP 403 only to automated fetch). Author: **Ryan Lopopolo**. Every
granular figure is confirmed verbatim and is now safe to say on camera:

| Claim | Verbatim from the post |
|---|---|
| duration | *"Over the past five months"* — first commit **late August 2025** |
| scale | *"on the order of a million lines of code"* |
| PRs | *"roughly 1,500 pull requests have been opened and merged"* |
| team | *"a small team of just three engineers"*, throughput **rose** as it *"grown to now seven engineers"* |
| throughput | *"an average throughput of 3.5 PRs per engineer per day"* |
| speed | *"about 1/10th the time it would have taken to write the code by hand"* |
| manual code | *"humans never directly contributed any code"* |

**Harness detail worth using on camera** (all primary, all new to us):

- **AGENTS.md is a table of contents, not an encyclopedia** — *"give Codex a map, not a
  1,000-page instruction manual."* Roughly **100 lines**, pointing into a structured
  `docs/` tree that is the system of record. They tried one big AGENTS.md and it failed:
  *"Context is a scarce resource"*, *"Too much guidance becomes non-guidance"*, *"It rots
  instantly."* **This is the single best real-world citation for Episode 3's Context layer.**
- **Legibility as a design goal** — *"anything it can't access in-context while running
  effectively doesn't exist."* Knowledge in Google Docs or Slack is invisible to the agent.
- **Observability wired into the harness** — Chrome DevTools Protocol in the agent runtime;
  per-worktree ephemeral logs/metrics the agent queries with LogQL and PromQL. Ep 7.
- **Architecture enforced mechanically** — fixed layers (Types → Config → Repo → Service →
  Runtime → UI) with permissible dependency edges, checked by Codex-written custom linters
  whose *error messages inject remediation instructions into agent context*. Ep 7 Governance.
- **Entropy and garbage collection** — the team used to spend *"every Friday (20% of the
  week) cleaning up 'AI slop'"*; that didn't scale, so they encoded *"golden principles"*
  and run background cleanup agents. Ep 5 / Ep 7.
- Single Codex runs of *"upwards of six hours"*; agent-to-agent review; a self-described
  **Ralph Wiggum Loop**.

**Honest caveat the post states itself, and we should repeat:** this end-to-end autonomy
*"depends heavily on the specific structure and tooling of this repository and should not
be assumed to generalize without similar investment—at least, not yet."*

---

## 2. ARC-AGI-3

- Competition: https://arcprize.org/competitions/2026/arc-agi-3
- Kaggle: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3
- Technical report: https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf (arXiv 2603.24621)
- Scoring methodology: https://docs.arcprize.org/methodology
- Human baseline study: https://arcprize.org/blog/arc-agi-3-human-dataset

ARC-AGI-3 measures **interactive, agentic** reasoning — the agent is dropped into a
game with no rules explained and must infer the goal itself. Different task from
ARC-AGI-2's static grid puzzles.

### RHAE — the actual metric (docs.arcprize.org/methodology)

Relative Human Action Efficiency, pronounced "ray". Scores **action efficiency vs a
human baseline**, not just solve rate.

    level_score = min(1.15, (human_baseline_actions / ai_actions) ** 2)

- Squared term: 2x the actions → 1/4 the score. Brute force is punished hard.
- Capped at 1.15 (an agent beating humans gets at most 115% on a level).
- Game score = weighted average of level scores, weight = 1-indexed level number
  (later/harder levels count more).
- Incomplete games cap the ceiling: 4 of 5 levels → max (1+2+3+4)/(1+2+3+4+5) = 66.7%.
- Final score = average of game scores. **Scale is 0–100%.**
- Human baseline = median first-time player per level, 458 participants in SF.
  Humans score ~100% by construction.

**Why RHAE matters for the narrative:** an agent can *solve* levels and still score
near zero, because inefficiency is punished quadratically. Solving is necessary but
nowhere near sufficient. This explains the Duck numbers in §2.2.

### 2.1 THE SCALE TRAP — read this before making any chart

There are **three incompatible scales** in circulation. Mixing them produces a chart
that is simply wrong. This is the single easiest way to embarrass yourself on camera.

**Scale A — official leaderboard / semi-private set.** The real number.

| System | Score | Source |
|---|---|---|
| GPT-5.5 | **0.43%** | arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis (primary) |
| Opus 4.7 | **0.18%** | same (primary) |
| Tufa Labs "Duck" | **1.21%** *(self-reported)* | x.com/tufalabs/status/2072336849465417747 |

The GPT-5.5 and Opus 4.7 figures are **primary** (ARC Prize's own blog): *"tested with the
semi-private dataset"*, *"All reported scores use the standard ARC-AGI-3 harness."*
Published **01 May 2026**.

> **Duck's 1.21% is SELF-REPORTED, not on an ARC Prize primary page (re-checked
> 2026-07-18).** Verbatim from Tufa's X post: *"We hit 1.21% with our lightweight harness."*
> The arcprize Milestone-1 blog explicitly states **no numerical scores**, and the
> GPT-5.5/Opus analysis page **does not list Duck**. A secondary aggregator (digg.com)
> separately frames the leaderboard as moving *"from 0.68% to 1.17%"* — note **1.17 ≠ 1.21**;
> the discrepancy is unreconciled. On camera: attribute 1.21% to *"Tufa Labs' own report"*,
> not to the ARC Prize leaderboard, and drop the 0.68→1.17 figure unless a primary source
> confirms it.

**Scale B — public 25-game set.** Self-reported, iterate-able, much higher.

| System | Score | Source |
|---|---|---|
| Executable World Models + GPT-5.5 (high) | **58.12%**, solved 15/25 games | arxiv.org/abs/2605.05138 |
| Executable World Models + GPT-5.4 (high) | **41.29%**, solved 8/25 games | same |
| Symbolica Agentica | **36.08%** (author calls it unverified) | symbolica.ai/blog/arc-agi-3 |
| Tufa Labs "Duck" | **1.6002 ± 0.4475** "mean score across all public games" | tufalabs.ai/research/duck-harness/ |

**Scale C — Kaggle public leaderboard.** ~1.86 top (YUTO KOJIMA), its own scale, on
~50% of test data. Final standings will differ. Never compare to Scale A or B.

**The gap between Scale A and Scale B is the story, not an error.** EWM scores 58.12%
on public games; the best *leaderboard* number in the field is ~1.2%. The EWM paper is
candid about exactly this:

> "Performance on the private validation set, which is not yet available to us,
> remains to be tested."
> "The private validation set is the decisive test of whether the current
> ARC-AGI-3-specific tools are genuinely game-general."

Teach that. Public-set numbers are hill-climbable; leaderboard numbers are not.

**OPEN QUESTION — do not assert either way.** Duck's *"mean score across all public
games is 1.6002 +/- 0.4475"* does **not** state its units. The post never calls it a
percentage or an RHAE figure. It sits oddly against Symbolica's 36.08% and EWM's
58.12% on the same public set. A plausible reading — consistent with Duck's 1.21%
leaderboard figure and with the post's *"some games being solved consistently for over
40% of the levels"* — is that Duck **solves levels but inefficiently**, and RHAE's
squared penalty crushes the score toward zero. That reading is **inference, not
citation.** Say "Duck reports a mean public-game score of 1.6002; the write-up doesn't
state the units" and move on.

### 2.2 Milestone 1 (arcprize.org/blog/arc-prize-2026-milestone-1)

$37.5K prize, ran through **June 30**. Top three:
1. Tufa Labs — "The Duck"
2. Reki
3. Md Boktiar Mahbub Murad — "forge"

Duck is the only winner using the **agent-writes-code** approach.

**UNVERIFIED — the blog does NOT state the rules.** No model-size limit, cost limit,
compute limit, or open-source mandate is given, and **no judging criteria are
published**. It gives no numerical scores or dataset spec either. So:
**do not claim why Duck won.** The post highlights Duck's features as *observations*,
not as stated reasons. If you need a reason on camera, say "the criteria weren't
published."

### 2.3 Duck Harness (tufalabs.ai/research/duck-harness)

- Write-up: https://tufalabs.ai/research/duck-harness/
- GitHub org: https://github.com/Tufalabs
- Kaggle notebook: https://www.kaggle.com/code/jeroencottaar/tufa-labs-duck-harness-june-30-milestone-winner
- Published **July 1, 2026**. Open source.

Verified design facts:
- Built on **Qwen 3.6 27B FP8**.
- *"a minimal coding harness with a Python interpreter"*; game perception **through images**.
- Observations arrive as Python variables; the model *"can inspect these variables with
  tool calls, evaluate pre-built helper functions."*
- **Infinite play via eviction**: *"context is kept short by automatically evicting the
  oldest messages"* — keeps system prompt + recent history, never exhausts context.
- *"the duck harness is an order of magnitude cheaper on each game"* — **compared
  specifically against the Executable World Models agent using GPT-5.4.**

**Do not claim "hand-crafted tools hurt."** A claim circulating in secondary sources says
Tufa found hand-built tools hurt and improvisation worked better. The primary post
**does not say this, and it leans the other way**: it mentions pre-built helper
functions, frames minimalism as a *practical constraint* (*"restricted to use small
open-source models"*) rather than a performance advantage, and states:

> "solvability of a game being dependent on model capability, while the cost is mostly
> dictated by the harness."

That quote is more interesting than the rumor, and it's a useful counterweight for a series
about harnesses: **Tufa's own position is that the model determines whether you** ***can***
**solve it, and the harness determines what it** ***costs***. Put that on screen. Then use
DeepAgents (§1.1) as the counterweight — same model, +13.7 points from harness alone.
The honest synthesis is that both are true and the boundary is the open question.

### 2.4 Executable World Models (arxiv.org/abs/2605.05138)

- **"Executable World Models for ARC-AGI-3 in the Era of Coding Agents"**
- Author: **Sergey Rodionov**. v1 **May 6, 2026**, v2 **June 6, 2026**.
- Code: https://github.com/astroseger/arc-3-agents-baseline1

This is also the approach Duck benchmarks its cost against.

Abstract, verbatim:

> "We evaluate an initial coding-agent system for ARC-AGI-3 in which the agent
> maintains an executable Python world model, verifies it against previous
> observations, refactors it toward simpler abstractions as a practical proxy for an
> MDL-like simplicity bias, and plans through the model before acting."

Design: scripted controller, predefined world-model interfaces, verifier programs, a
plan executor — **but no hand-coded game-specific logic.** Each game got a single
playthrough, no restarts, no access to previous runs.

Results (public 25-game set): **GPT-5.5 high → 58.12% RHAE, 15/25 solved.**
**GPT-5.4 high → 41.29% RHAE, 8/25 solved.**

Cost, verbatim: *"a single ChatGPT Pro subscription, priced at USD 200 per month...was
sufficient to run full experiments for roughly two to eight games."* This is the cost
Duck claims to beat by an order of magnitude.

**This paper is the strongest real support for the code-as-harness thesis** — the
world model *is* executable Python, verified and refactored by the agent. Cite this,
not a made-up paper.

---

## 3. Harness taxonomy — ETCLOVG

**ETCLOVG is real** and matches the seven layers: Execution environment, Tool
interface, Context management, Lifecycle/Orchestration, Observability, Verification,
Governance. It extends prior six-component frameworks by treating **observability and
governance as independent architectural concerns**. Coverage: **110+ papers, 23+
deployed systems.**

Status: **"Agent Harness Engineering: A Survey", under review as a TMLR submission.**
Say **"under review"**, not "published".

- https://openreview.net/forum?id=3hXEPbG0dh
- https://openreview.net/pdf?id=eONq7FdiHa
- https://ai-eval.org/deep-dive/openreview-agent-harness-engineering-survey

**NOT CONFIRMABLE BY AUTOMATION — 3 attempts, now closed as such (2026-09-09).**
OpenReview gates the forum page *and* its public API (`api2.openreview.net`) behind a
bot-verification challenge, which returns `ChallengeRequiredError` 403. The "under
review / TMLR" status therefore comes from search results and the ai-eval.org write-up,
**never from OpenReview itself.**

**This no longer blocks anything.** The scripts were changed to say **"an OpenReview
preprint by Li et al."** and dropped the TMLR claim entirely, so the safe wording is
already in place. Confirming the venue in a signed-in browser would only let you upgrade
that phrasing — it is optional polish, not an open risk.

Related, for the Verification layer: "From Failed Trajectories to Reliable LLM Agents:
Diagnosing and Repairing Harness Flaws" — https://arxiv.org/html/2606.06324v1

---

## 4. Frameworks

### Verified

- **Vercel AI SDK 7** — published **June 25, 2026**, generally available. Introduces
  **experimental** harness abstractions and **`HarnessAgent`**: one API to run
  configured harnesses (Claude Code, Codex, Pi), normalizing skills, sandboxes,
  sessions, permission flows, compaction, and sub-agents. `HarnessAgent.generate()`
  and `.stream()` are AI SDK–compatible. **Say "experimental"** — the SDK is GA, the
  harness API is not.
  - https://vercel.com/blog/ai-sdk-7
  - https://ai-sdk.dev/docs/ai-sdk-harnesses/overview
  - https://vercel.com/changelog/program-agent-harnesses-with-ai-sdk
  - Adapters: https://vercel.com/changelog/deepagents-and-opencode-harness-adapters

- **Mastra** — real, TypeScript. Hit **1.0 in January 2026**. Ships agents, workflows,
  memory, evals, observability. Production users cited: **Replit, PayPal, Sanity**.
  https://mastra.ai/ , https://github.com/mastra-ai/mastra

  **Be precise about Mastra's claim.** It is a memory result: observational memory
  compressing 5–40x more context into the same window at **~95% on LongMemEval**.
  That's a **vendor claim on a memory benchmark**, not a harness ranking — attribute
  it to Mastra if you use it at all, and never present it as a harness leaderboard.

### Landscape (secondary sources only — safe as orientation, not as ranking)

The commonly-listed 2026 field: LangGraph, OpenAI Agents SDK, Claude Agent SDK,
Google ADK, Pydantic AI, CrewAI, Strands Agents, Mastra, Vercel AI SDK, Microsoft
Agent Framework. Rough positioning, per comparison write-ups:

- **LangGraph** — graph-based, explicit control over long-running multi-actor workflows.
- **Pydantic AI** — type safety and validation, minimal orchestration ceremony.
- **CrewAI** — role-based multi-agent teams.
- **Strands / OpenAI Agents SDK / Claude Agent SDK / Google ADK / Microsoft Agent
  Framework** — ecosystem-aligned picks (AWS / OpenAI / Anthropic / Google / Microsoft).

Sources: https://www.speakeasy.com/blog/ai-agent-framework-comparison/ ,
https://www.langchain.com/resources/ai-agent-frameworks (LangChain's own — biased)

**These are editorial characterizations, not benchmarks. Present as "how people
describe the tradeoffs", never as measured rankings.** No verified head-to-head
benchmark of these frameworks exists in my sources.

---

## 5. Further reading

- Awesome list: https://github.com/ai-boost/awesome-harness-engineering
- Survey dataset: https://huggingface.co/datasets/GloriaaaM/LLM-Agent-Harness-Survey
- Harness survey & taxonomy notes: https://agentic-ai.readthedocs.io/en/latest/AgentHarness/llm-harness-survey/
- The harness is the reliability layer: https://www.antoinebuteau.com/the-harness-is-the-reliability-layer/
- Harness vs framework: https://atlan.com/know/ai-agent/agent-harness-vs-agent-framework/
- ReAct: https://arxiv.org/abs/2210.03629
- Reflexion: https://arxiv.org/abs/2303.11366
- Tree of Thoughts: https://arxiv.org/abs/2305.10601

---

## 6. Sourcing rules

- **Only cite what's in this file or `CLAIMS.csv` with a primary source.** If a paper,
  tool, or number isn't listed here, verify it against the primary source before using it —
  never from memory.
- **Prefer the issuing organization's own pages over aggregators.** ARC Prize's own blog
  gives **GPT-5.5 = 0.43%** and **Opus 4.7 = 0.18%** on the semi-private set with the
  standard harness. If you cite an aggregator (e.g. llm-stats.com) at all, say
  "self-reported to an aggregator, unverified."
- **Say "self-reported"** for any number not published by the benchmark's own organization
  (Duck's 1.21%, Symbolica's 36.08%).
- **arXiv IDs are YYMM.NNNNN** — a 2026 paper is `26MM.NNNNN`; there is no such form as
  `2026.xxxxx`. Verify IDs on arxiv.org; local copies live in `sources/`.

---

## 7. The 2026 "harness effect" literature (added 2026-09-12)

Per-claim rows are in `CLAIMS.csv` (verified_date 2026-09-12 = fetch date; re-read the
primary before relying on any of them). These are additional evidence and a counterweight
to the rest of this file, not corrections.

Taken together they sharpen the thesis to: **the model sets the ceiling on accuracy; the
harness sets cost and reliability; harness gains are real, sometimes large, and
model-specific.**

### 7.1 Stop Comparing LLM Agents Without Disclosing the Harness — arXiv 2605.23950 (2026-05-07)
- https://arxiv.org/abs/2605.23950 — Yunbei Zhang et al.
- Model fixed, harness changed: TerminalBench 2 pass@1 **69.7 → 77.0** (+7.3), GPT-5.4
  (high), "automated harness optimization" — **cited by this paper from Lin et al. 2026
  (AHE)**, not run by these authors. Up to **15 pts** scaffold-only variation on
  SWE-bench Verified (third-party monitoring).
- Proposes the **ETCSOVG** seven-layer disclosure standard and a model×harness variance
  decomposition (HV/MV ratio, ranking reversals, partial η²).
- **Caveat for camera:** the +7.3 is second-hand inside the paper; say "as reported by".
  ETCSOVG ≠ the series' ETCLOVG (S = Scheduling ≈ L = Lifecycle).

### 7.2 Harness-Bench — arXiv 2605.27922 (2026-05-27)
- https://arxiv.org/abs/2605.27922 — Yao et al. (Qihoo 360). Code/data:
  https://github.com/Qihoo360/harness-bench
- 106 sandboxed offline tasks, 6 harnesses × 8 models, 5,194 trajectories.
  TaskScore = Security × Completion × Process. **NanoBot 76.2% vs OpenClaw 52.4%**
  (23.8 pts); Codex reference 80.4%. Conclusion: attribute capability to
  model×harness *pairs*.

### 7.3 Scaffold Effects on GAIA — arXiv 2606.08529 (2026-06-07)
- https://arxiv.org/abs/2606.08529 — Jason Starace. ReAct vs Planner-Actor-Rater vs
  Planner-then-executor; Claude Opus 4.7 / Sonnet 4.6 / Haiku 4.5, Gemini 3.1 Pro
  Preview, GPT-5.5.
- Verbatim: *"Scaffold choice alone moves measured accuracy by as much as 28 percentage
  points within a single model (Opus, Level 2)."* Pre-registered ≥10-pt hypothesis
  confirmed. Code release not stated.

### 7.4 The Scaffold Effect in Coding Agents — arXiv 2607.22585 (2026-06-08)
- https://arxiv.org/abs/2607.22585 — Vats & Golev. Terminal-Bench **Pro**, 50 stratified
  tasks, 3 harnesses (Goose, OpenCode, OpenHands-SDK) × 2 models (Qwen 3.6 Plus, MiniMax
  M2.5) = 300 trials.
- Pass-rate variation **0–8 pts**; **tokens per solved task up to 40×** (Goose 28,142 /
  36,950 vs OpenCode 1,147,740 / 1,546,977). Failure taxonomy
  REASON/VERIFY/TIME/MAX_TURNS/HANG/ERROR. Logs and configs released (anonymised).
- Same shape as the Ep 4 Wordle A/B token result (`RUNS.md`): the harness moves cost
  far more than it moves the pass rate.

### 7.5 Does the Harness Matter? — Agents' Last Exam blog (2026-06-11)
- https://agents-last-exam.org/blogs/harness-matters — OpenClaw vs ALE-Claw (stripped)
  vs Codex, Cursor, Droid; GPT-5.5, Claude Opus 4.7 and others.
- Verbatim: *"Model sweep spans 18.0 percentage points, while fixed-model harness sweeps
  span only 5 to 6 points."* ALE-Claw matched OpenClaw's accuracy with **44% fewer input
  tokens, 41% lower cost, 60% less wall-clock**.
- **This is the strongest counterweight in the literature** — stronger than the Tufa
  quote in §2.3. It supports the same reading: the model sets the ceiling; the harness
  sets cost. For show notes / errata, not the cuts (D-008).

### 7.6 Survey: From Question Answering to Task Completion — arXiv 2606.20683 (2026-06-14)
- https://arxiv.org/abs/2606.20683 — Guo et al. Six runtime responsibilities
  (observation, context, control, action, state, verification); open problems include
  **model–harness co-evolution** and harness generalization across domains.

### 7.7 Source-code study of eleven coding harnesses — arXiv 2609.00006 (submitted 2026-07-15, CC BY 4.0)
- https://arxiv.org/abs/2609.00006 — Barbaste, Darrigol, Vu, Wiltberger. Claude Code,
  Codex CLI, Gemini CLI, Mistral Vibe, OpenHands, Aider, Mini-SWE-Agent, Hermes, Pi,
  OpenCode, OpenClaw.
- Seven subsystems, **29 patterns**, 13 observations, 18 recommendations, a **90-line
  Python minimum-viable harness**. Observations usable verbatim: no system imports a
  general agentic framework; none uses embedding-based code retrieval; loop
  sophistication does not predict benchmark performance; SKILL.md 9/11 vs MCP 8/11.
- Corroborates the ETCLOVG-style layering in §3 from source code rather than surveys.

### 7.8 Niklaus — Meta-Harness on SWE-bench Pro and Harvey's legal benchmark (2026)
- https://github.com/JoelNiklaus/harness-optimization (repo README; blog linked there;
  5,000 rollouts on HF `joelniklaus/CodingBenchmarkResults`).
- SWE-bench Pro pass@1: GLM-5.2 **23.2 → 52.4%**; Gemma 4 **15.2 → 36.0%**. Harness
  rankings across models: **Spearman −0.05** — a harness tuned on one model does not
  transfer. **Status: repo-README-verified, not a paper; say so.**

### 7.9 Artificial Analysis Coding Agent Index (launched May 2026; v1.5 by Sept 2026)
- https://artificialanalysis.ai/methodology/coding-agents-benchmarking — first public
  leaderboard of **model + harness stacks**; index = mean of DeepSWE v1.1, Terminal-Bench
  4.0, SWE-Atlas-QnA; tracks tokens and cost.
- The widely quoted "same model, 32× cost spread ($0.07–$2.26 per task)" is from a
  **secondary** post (agentconn.com) — find the AA primary before quoting.

### 7.10 Housekeeping facts
- **Terminal-Bench moved:** the runner docs now default to 4.0 (Harbor); the papers above
  cite 2.0, 2.1 and "Pro". Always state the version.
- **DeepSeek open-sourced its harness** (`dsh` v0.1, MIT, 2026-08-20 — InfoQ, secondary;
  find the repo before citing).
- **Inspect AI 0.3.12 "reliability score"** — **REFUTED 2026-09-12.** A secondary blog
  dated the feature to a July 2026 release of Inspect AI 0.3.12. PyPI shows 0.3.12 was
  released **2024-05-31**, and the current version on 2026-09-04 is 0.3.263; neither the
  project description nor the release list mentions a reliability score, recovery rate,
  or harness adapters. The claim is dropped, not merely unverified. Do not cite.

---

## Last verified
2026-07-18 — verified against primary sources (browser/WebFetch + local PDFs):
Meta-Harness (arXiv 2603.28052: title, authors, 2026-03-30, "TerminalBench-2" spelling,
all three results), GPT-5.5 0.43% / Opus 4.7 0.18% (arcprize analysis, semi-private,
standard harness, 01 May 2026), Milestone-1 **$37.5K** + top-three (arcprize blog),
Duck page title + Qwen 3.6 27B FP8 + 1.6002±0.4475 unit-less + all quotes (tufalabs).
Duck's **1.21% is self-reported** (Tufa X post), not on any ARC Prize primary page — §2.1.
**Cleared 2026-09-09 in a real browser:** openai.com Codex granular figures (§1.3) — all
confirmed verbatim, nothing left to hedge on camera.

**Closed as not-confirmable:** TMLR status (§3) — OpenReview gates its site *and* API
behind a bot challenge. The scripts already dropped the TMLR claim, so nothing depends
on it.

**Still outstanding:** Duck's 1.6002 units (§2.1). Per-claim detail: `CLAIMS.csv`.

**2026-09-12 — §7 added** (nine harness-effect sources, fetched via WebFetch; verified_date in
`CLAIMS.csv` is the fetch date). Two items are secondary and one unverified — marked in §7.
Episodes unchanged (D-008).
