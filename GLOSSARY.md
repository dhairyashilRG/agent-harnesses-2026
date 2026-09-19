# Glossary — AI Agent Harness Series

Terms are defined as the 2026 sources use them. Where usage is contested, that's
noted rather than papered over. Citations: `resources_2026.md`.

---

## The four words people mix up

Put this on screen in Episode 1 and never let it drift.

| Term | What it is | One-line test |
|---|---|---|
| **Model** | The weights. Given tokens, returns tokens. | Can it be swapped for another vendor's? Then it's the model. |
| **Harness** | The code around the model deciding what it stores, retrieves, and sees. | Does it survive a model swap? Then it's the harness. |
| **Agent** | Model + harness, running a loop toward a goal. | Does it take actions and observe results? Then it's an agent. |
| **Framework** | A library for *building* harnesses. | Is it a dependency in your `requirements.txt` / `package.json`? Then it's a framework. |

**Scaffold** — older word, mostly synonymous with harness. Common through 2024–2025;
"harness" won in 2026 once OpenAI and the survey literature standardized on it. If a
source says scaffold, read harness.

**The definition to quote** (Meta-Harness, arXiv 2603.28052) — the harness is:

> "the code that determines what information to store, retrieve, and present to the model"

That's the cleanest one-sentence definition in the literature. Use it.

---

## Core concepts

**Harness engineering** — designing the harness rather than the prompt or the model.
Named as a discipline by OpenAI on 2026-02-11. Predecessors: prompt engineering
(2022–2024) → context engineering → harness engineering (2025–2026).

**ETCLOVG** — the seven-layer harness taxonomy from "Agent Harness Engineering: A
Survey" (110+ papers, 23+ deployed systems; under review, TMLR — **verify status**):

| Layer | Scope |
|---|---|
| **E**xecution environment | Sandboxes, isolation |
| **T**ool interface | Protocols, integration |
| **C**ontext management | Memory, persistence |
| **L**ifecycle / Orchestration | State, task loops |
| **O**bservability | Traces, cost tracking |
| **V**erification | Evaluation, regression loops |
| **G**overnance | Permissions, audit |

Its contribution over earlier six-component frameworks: **Observability and Governance
are independent architectural concerns**, not afterthoughts.

**ReAct** — Reason + Act. The base agent loop: thought → action → observation → repeat.
arXiv 2210.03629 (2022). Still the skeleton under every 2026 harness.

**Reflexion** — agent reflects on failures in natural language and retries.
arXiv 2303.11366 (2023).

**Tree of Thoughts** — explore multiple reasoning branches, backtrack.
arXiv 2305.10601 (2023).

**Context eviction** — dropping oldest messages to keep context bounded, so a
long-running agent never hits the window. Duck's *"infinite play via eviction"*:
keep the system prompt + recent history, pop the rest.

**Compaction** — summarizing history instead of dropping it. Compare to eviction:
eviction is lossy and cheap, compaction is lossy and expensive. AI SDK 7's
`HarnessAgent` normalizes compaction as a first-class concern.

**Trace mining** — reading execution traces to find failure modes, then fixing the
harness. Manual version: LangChain used LangSmith traces to find failures and gained
+13.7 points. Automated version: Meta-Harness.

**Doom loop** — an agent repeating an ineffective action indefinitely (re-editing the
same file, re-running the same failing command). DeepAgents ships
`LoopDetectionMiddleware` against it. See `TROUBLESHOOTING.md`.

**Agent-writes-code** — the action the model emits *is* Python, executed in a REPL,
with stdout fed back. Duck's approach; the only one among Milestone 1 winners.

**Executable world model** — the agent's model of the environment, maintained as
runnable Python, verified against observations and refactored toward simpler
abstractions. arXiv 2605.05138.

**Middleware** — harness code that intercepts the agent loop. DeepAgents' three:
`PreCompletionChecklistMiddleware` (verification), `LoopDetectionMiddleware`
(lifecycle), `LocalContextMiddleware` (context injection).

**Outer loop / inner loop** — the inner loop is the agent solving a task (ReAct). The
outer loop is the process improving the harness itself (Meta-Harness). Two nested
loops; keep them visually distinct.

---

## Evaluation vocabulary

**ARC-AGI-3** — interactive/agentic reasoning benchmark. The agent is dropped into a
game with **no rules explained** and must infer the goal. Distinct from ARC-AGI-2's
static grid puzzles.

**RHAE** — *Relative Human Action Efficiency*, pronounced **"ray"**. ARC-AGI-3's metric.
Scores action efficiency against a human baseline, not just solve rate:

    level_score = min(1.15, (human_baseline_actions / ai_actions) ** 2)

- **Squared** → 2x the actions = 1/4 the score; 10x = ~1/100.
- **Capped at 1.15** → beating humans earns at most 115% on a level.
- **Game score** = weighted average of levels, weight = 1-indexed level number.
- **Final** = mean of game scores, 0–100%.

**The RHAE point:** an agent can *solve* a level and still score ~0 by flailing.
Solving is necessary, nowhere near sufficient.

**Human baseline** — median first-time player per level, from a 458-participant study
in San Francisco. Humans score ~100% **by construction**.

**Semi-private set** — ARC's held-out evaluation set. Official leaderboard numbers come
from here. **Not** hill-climbable.

**Public set** — the 25 public ARC-AGI-3 games. Teams iterate against these directly, so
scores run far higher. A public score is a hypothesis, not a result.

**The three scales — never chart together:**

| | Set | Top number |
|---|---|---|
| **A** | Semi-private leaderboard, standard harness | ~1.2% (Duck) |
| **B** | Public 25-game set, self-reported | 58.12% (EWM + GPT-5.5) |
| **C** | Kaggle public leaderboard | ~1.86, own scale, ~50% of test data |

**Terminal Bench 2.0** — agentic coding benchmark. DeepAgents: 52.8 → 66.5 with the
model fixed. Meta-Harness's automated harnesses also beat hand-engineered baselines
here. The one benchmark where both the manual and automated stories land.

**Held-out model** — a model the harness wasn't tuned on. Meta-Harness's +4.7 points
averaged across **five held-out models** is a generalization claim, which is why it
matters more than a single-model number.

---

## Words to use carefully on camera

- **"Self-reported"** — say it for any number not from arcprize.org. llm-stats.com
  lists 0 verified / 3 self-reported for its GPT-5.6 rows.
- **"Under review"** — not "published", for the ETCLOVG survey (TMLR).
- **"Experimental"** — AI SDK 7 is GA; its `HarnessAgent` harness API is not.
- **"Unstated"** — Duck's 1.6002 mean has no units in the source. Don't supply them.
- **"As of July 2026"** — every number in this series has a shelf life.
