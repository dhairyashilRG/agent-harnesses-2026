# Failure Modes & Fixes

Every failure here is **real** — either hit while building this series' demos, or
documented in a cited 2026 source. Nothing invented. Each maps to an ETCLOVG layer so
it slots into Episode 3's colour scheme, and each has a place in Episode 7.

Sources: `resources_2026.md`. Terms: `GLOSSARY.md`.

---

## 1. Reasoning model returns empty content

**Layer:** Tool interface / Lifecycle
**Status:** hit live, 2026-07-17, building `duck_harness_simplified.py`

**Symptom.** The API returns `200 OK`. `content` is `""`. Nothing crashes. The agent
loop silently does nothing.

**Diagnosis.** `deepseek-v4-flash` is a reasoning model: it spends completion tokens on
`reasoning_content` *before* emitting any `content`. With `max_tokens` too low it burns
the entire budget thinking and returns an empty string with `finish_reason: "length"`.
Our first live call came back with `reasoning_tokens: 10` and no content at all.

**Fix.** Budget for reasoning (`MAX_TOKENS = 2000`), and **fail loudly** rather than
looping on empty strings:

```python
if choice.get("finish_reason") == "length" and not choice["message"].get("content"):
    raise RuntimeError(
        "Model hit the token limit before emitting content — raise MAX_TOKENS."
    )
```

**The lesson worth saying on camera.** A 200 with an empty body is the worst class of
harness bug: no exception, no signal, just an agent that quietly accomplishes nothing.
**Your harness must distinguish "the model said nothing" from "the model is done."**

---

## 2. Doom loops

**Layer:** Lifecycle / Orchestration
**Status:** documented — LangChain shipped a fix

**Symptom.** The agent re-edits the same file, or re-runs the same failing command,
forever. Burns budget, never converges.

**Fix.** LangChain's `LoopDetectionMiddleware` tracks file edits and detects the
repetition. It was one of three harness changes behind **52.8 → 66.5** on Terminal
Bench 2.0 with the model held fixed.

**The lesson.** The model can't see it's looping — it has no memory of the shape of its
own behaviour, only the context you show it. **Loop detection is a harness
responsibility, categorically.** No prompt fixes this.

---

## 3. Context overflow on long-running agents

**Layer:** Context management
**Status:** documented — two different real fixes

**Symptom.** Long-running agents hit the context window and die, or start dropping the
information that mattered.

**Fix A — eviction (Duck).** *"context is kept short by automatically evicting the
oldest messages."* Keep the system prompt + recent history, pop the rest. Cheap and
lossy. Duck calls the result **"infinite play"** — the agent plays indefinitely.

```python
def _evict(self):
    """Duck's trick: keep the system prompt, drop the oldest turns."""
    if len(self.messages) > self.keep_turns + 1:
        self.messages = [self.messages[0]] + self.messages[-self.keep_turns:]
```

**Fix B — better context management (Meta-Harness).** Its discovered harness beat a
SOTA context management system by **+7.7 points while using 4x fewer context tokens.**

**The lesson.** Efficiency and quality are **not** necessarily a tradeoff — Meta-Harness
got both. And note the counterintuitive part: a bigger context window is not the fix.
Duck's answer to "we ran out of context" is to **deliberately throw context away.**

---

## 4. Tool hallucination

**Layer:** Tool interface / Context management
**Status:** documented — LangChain shipped a fix

**Symptom.** The agent invents tools, or misuses real ones, because it's guessing at
what its environment contains.

**Fix.** LangChain's `LocalContextMiddleware` maps directories and discovers tools,
injecting the real environment into context. One of the three changes behind +13.7
points.

**The lesson.** A model guessing at its environment will hallucinate. **Tell it what's
actually there** — don't hope it infers correctly.

---

## 5. Trusting the agent's self-report

**Layer:** Verification
**Status:** designed against in every demo here

**Symptom.** The agent says "FINAL: 816" and you believe it. It says it verified. It
didn't.

**Fix.** Check independently, in code the agent cannot touch:

```python
# Independent check — the harness verifying the agent, not trusting it.
truth = sum(n for n in range(1, 101) if n % 2 == 0 and n % 3 == 0)
ok = answer is not None and str(truth) in answer
```

`self_improving_harness.py` goes further — **every task check is programmatic**. No LLM
grades itself anywhere in this series.

LangChain's version: `PreCompletionChecklistMiddleware`, forcing self-verification
before the agent can declare done. Their system prompt adds a build-verify loop: plan →
implement with tests in mind → verify → fix.

**The lesson.** *"Self-verification & tracing help a lot"* — LangChain. Verification is
an architectural layer, not a nice-to-have.

---

## 6. Executing model-written code unsandboxed

**Layer:** Execution environment / Governance
**Status:** designed against in every demo here

**Symptom.** You `exec()` text a language model wrote. In your process. With your
filesystem.

**Fix, minimum viable.** Subprocess + timeout, as in all demos here:

```python
proc = subprocess.run(
    [sys.executable, path],
    capture_output=True, text=True, timeout=self.timeout,
)
```

This is *the floor*, not a real sandbox — no network isolation, no filesystem
restriction, no memory cap. It's honest to say so on camera. AI SDK 7's `HarnessAgent`
normalizes **sandboxes and permission flows** as first-class harness concerns, which is
the direction to point people.

**The lesson.** The Execution layer exists because **the agent-writes-code approach means
running untrusted text.** Duck, EWM, DeepAgents, and every demo here all do it. Show the
boundary explicitly.

---

## 7. Silent model substitution

**Layer:** meta — a *human* failure mode
**Status:** I did this, mid-series. Worth two minutes on camera.

**Symptom.** A test fails against `deepseek-v4-flash`. Swapping to `deepseek-chat`
makes it pass. Ship it.

**What actually happened.** `GET /v1/models` later showed `deepseek-v4-flash` and
`deepseek-v4-pro` are the only real models. The substitution was **both unnecessary and
wrong** — and it hid the real bug, which was failure mode #1 above. A green test bought
by changing the thing under test is worse than a red one.

**Fix.** Check what's actually available. Fix the harness, not the test.

**The lesson.** This is the human version of every failure on this page: **when the
signal is inconvenient, the temptation is to change the measurement.** Related, and
also worth saying: `self_improving_harness.py` currently has **nothing to mine** because
the baseline scores 4/4. The honest move was to report that, not to rig the tasks until
they failed.

---

## 8. Reading the wrong benchmark scale

**Layer:** meta — an evaluation failure mode
**Status:** nearly shipped this series with a chart that was simply wrong

**Symptom.** You chart ARC-AGI-3 scores and get 58.12% next to 1.21% and conclude
something dramatic.

**Diagnosis.** They're different sets. **58.12%** is EWM on the hill-climbable **public
25-game set**. **1.21%** is Duck on the **semi-private leaderboard**. Same benchmark
name, same metric name, ~48x apart, not comparable.

**Fix.** Always ask *which set*. See `resources_2026.md` §2.1 for all three scales.

**The lesson, and it's the best one in the series.** The EWM paper flags its own number:

> "Performance on the private validation set, which is not yet available to us, remains
> to be tested."

**A public-set score is a hypothesis. A leaderboard score is a result.** An author
saying so in their own abstract is what good reporting looks like.

---

## Quick reference

| # | Failure | Layer | Fix |
|---|---|---|---|
| 1 | Empty content from reasoning model | Tooling / Lifecycle | Budget tokens; fail loudly on `length` + empty |
| 2 | Doom loops | Lifecycle | `LoopDetectionMiddleware` |
| 3 | Context overflow | Context | Eviction (Duck) or better management (Meta-Harness) |
| 4 | Tool hallucination | Tooling / Context | Inject real environment (`LocalContextMiddleware`) |
| 5 | Trusting self-reports | Verification | Programmatic ground-truth checks |
| 6 | Unsandboxed execution | Execution / Governance | Subprocess + timeout, minimum |
| 7 | Silent model substitution | *human* | Fix the harness, not the test |
| 8 | Wrong benchmark scale | *evaluation* | Ask which set. Always. |
