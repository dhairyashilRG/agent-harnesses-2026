# AI Agent Harness — References

> **Source of truth for all claims is [`resources_2026.md`](resources_2026.md).** This file
> is a citation index only. Primary PDFs are archived locally in [`sources/`](sources/) and
> were re-downloaded and confirmed real on **2026-07-18**. Where a number appears below it
> is stated exactly as `resources_2026.md` has it — do not introduce numbers here that are
> not in that file.
>
> **arXiv year convention:** an ID like `26YY.NNNNN` is a **2026** paper (`25YY` = 2025,
> `24YY` = 2024). Citation counts and leaderboard percentages decay — check them live on
> recording day rather than trusting a memorized figure.

---

## 1. The three pillars (primary-sourced — see `resources_2026.md` §1)

### DeepAgents — controlled harness experiment
- LangChain blog, **2026-02-17**: https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering
- Terminal Bench 2.0: **52.8 → 66.5** (+13.7), Top 30 → Top 5, **model fixed** (`gpt-5.2-codex`).
- Verbatim: *"We only tweaked the harness and kept the model fixed."*

### Meta-Harness — automating the harness (`sources/meta-harness-2603.28052.pdf`)
- **arXiv 2603.28052** (2026-03-30): https://arxiv.org/abs/2603.28052
- Lee, Nair, Zhang, Lee, Khattab, Finn (Stanford / MIT / KRAFTON). Code: https://github.com/stanford-iris-lab/meta-harness
- +7.7 pts / 4x fewer tokens (text classification); +4.7 pts on 200 IMO-level problems across
  five held-out models; surpasses best hand-engineered baselines on **TerminalBench-2**.

### OpenAI Codex — harness engineering named (2026-02-11)
- Primary: https://openai.com/index/harness-engineering/ by **Ryan Lopopolo**
  *(403 to automated fetch; opened in a browser and **fully verified 2026-09-09**)*
- Secondary (corroborates core): https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/
- Confirmed: ~1M lines, no manually written source code, internal beta product, **five
  months** (first commit late Aug 2025), **~1,500 PRs**, **3 → 7 engineers**, **3.5
  PRs/engineer/day**, **~1/10th the time**; humans designed environments / intent / feedback.
- Richest harness material in the series: AGENTS.md as a ~100-line *map* into a `docs/`
  system of record, CDP + LogQL/PromQL observability, mechanically enforced architecture
  layers, and "golden principles" garbage collection. See `resources_2026.md` §1.3.

---

## 2. ARC-AGI-3 (see `resources_2026.md` §2 for the scale-trap discipline)

- Competition: https://arcprize.org/competitions/2026/arc-agi-3
- Technical report: **arXiv 2603.24621** (`sources/arc-agi-3-techreport-2603.24621.pdf`)
- Scoring methodology (RHAE): https://docs.arcprize.org/methodology
- Human baseline (458 participants, SF): https://arcprize.org/blog/arc-agi-3-human-dataset
- Frontier analysis, **01 May 2026**, semi-private set, standard harness:
  **GPT-5.5 = 0.43%**, **Opus 4.7 = 0.18%** (ARC Prize primary) —
  https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis
- **Milestone 1** ($37.5K; ran through June 30; top three: Tufa "Duck", Reki, "forge") —
  https://arcprize.org/blog/arc-prize-2026-milestone-1 *(no scores or criteria published)*

**Three incompatible scales — never chart together** (`resources_2026.md` §2.1):
- **A** semi-private leaderboard (~1%). **B** public 25-game set (EWM+GPT-5.5 **58.12%**).
  **C** Kaggle (own scale). ~48x apart.

> **ARC-AGI-1, not -3:** the 2024 competition's private eval rose 33% → **55.5%**
> (**arXiv 2412.04604**). Do not confuse with ARC-AGI-3. ARC-AGI-3 contrasts with
> **ARC-AGI-2**'s static grid puzzles (**arXiv 2505.11831**).

### Duck Harness (Tufa Labs)
- Write-up (2026-07-01): https://tufalabs.ai/research/duck-harness/ · Org: https://github.com/Tufalabs
- Title (verified): *"Duck Harness: Winning Solution for ARC-AGI-3 Milestone 1"*
- Base model **Qwen 3.6 27B FP8**; Python REPL; perception through images; oldest-first
  eviction ("infinite play"); *"an order of magnitude cheaper on each game"* vs EWM+GPT-5.4.
- **Score: 1.21% — SELF-REPORTED (Tufa X post), NOT on an ARC Prize page.** Public-games
  mean 1.6002 ± 0.4475 with **units unstated**. Authors' key line: *"solvability of a game
  being dependent on model capability, while the cost is mostly dictated by the harness."*
  Duck is **not** a continual-learning / pattern-library system.

### Executable World Models (`sources/executable-world-models-2605.05138.pdf`)
- **arXiv 2605.05138** (Rodionov; v1 2026-05-06, v2 2026-06-06): https://arxiv.org/abs/2605.05138
- Public 25-game set: **58.12% RHAE** (GPT-5.5 high, 15/25) / **41.29%** (GPT-5.4 high, 8/25).
  Cost: ran on a **$200/month** ChatGPT Pro subscription for *"roughly two to eight games."*
  Author flags the private set as untested (a model of honest reporting).

---

## 3. Harness taxonomy — ETCLOVG

- *"Agent Harness Engineering: A Survey"*, **Li et al. — an OpenReview preprint, 2026.**
  The seven-layer ETCLOVG taxonomy. Attribution verified via arXiv 2606.20683 ref [56].
  - https://openreview.net/forum?id=3hXEPbG0dh · https://openreview.net/pdf?id=eONq7FdiHa
  - Write-up: https://ai-eval.org/deep-dive/openreview-agent-harness-engineering-survey
  - **Say "an OpenReview preprint by Li et al." — do not claim TMLR.** OpenReview now
    gates both the site and its public API behind a bot-verification challenge, so venue
    status is not confirmable by any automated route; it needs a signed-in browser. The
    scripts no longer make the claim, so **nothing is blocked on this** — it stays open
    only if you want to upgrade the wording. The **"110+ papers / 23 systems"** figure
    belongs to **Meng et al.**, not this survey; attribute it there or cut it.
- Related survey (harness architecture): **arXiv 2606.20683**
  (`sources/survey-agent-system-harness-2606.20683.pdf`)
- Verification layer, related: *"From Failed Trajectories to Reliable LLM Agents"* —
  **arXiv 2606.06324** (`sources/diagnosing-harness-flaws-2606.06324.pdf`)

---

## 4. Foundational agent-loop papers (pre-cutoff, stable)

| Paper | Year | Venue | arXiv | Local |
|---|---|---|---|---|
| ReAct: Synergizing Reasoning and Acting | 2022 | ICLR 2023 | 2210.03629 | `sources/react-2210.03629.pdf` |
| Reflexion: Verbal Reinforcement Learning | 2023 | NeurIPS 2023 | 2303.11366 | `sources/reflexion-2303.11366.pdf` |
| Tree of Thoughts | 2023 | NeurIPS 2023 | 2305.10601 | `sources/tree-of-thoughts-2305.10601.pdf` |
| AutoGen | 2023 | — | 2308.08155 | — |

BibTeX (author lists verified against the papers):

```bibtex
@inproceedings{yao2023react,
  title={ReAct: Synergizing Reasoning and Acting in Language Models},
  author={Yao, Shunyu and Zhao, Jeffrey and Yu, Dian and Du, Nan and Shafran, Izhak
          and Narasimhan, Karthik and Cao, Yuan},
  booktitle={ICLR}, year={2023}, url={https://arxiv.org/abs/2210.03629}
}
@inproceedings{shinn2023reflexion,
  title={Reflexion: Language Agents with Verbal Reinforcement Learning},
  author={Shinn, Noah and Cassano, Federico and Gopinath, Ashwin and Narasimhan, Karthik
          and Yao, Shunyu},
  booktitle={NeurIPS}, year={2023}, url={https://arxiv.org/abs/2303.11366}
}
@inproceedings{yao2023tot,
  title={Tree of Thoughts: Deliberate Problem Solving with Large Language Models},
  author={Yao, Shunyu and Yu, Dian and Zhao, Jeffrey and Shafran, Izhak
          and Griffiths, Thomas L. and Cao, Yuan and Narasimhan, Karthik},
  booktitle={NeurIPS}, year={2023}, url={https://arxiv.org/abs/2305.10601}
}
```

---

## 5. Other 2026 papers cited in the series (all local in `sources/`)

| arXiv | Short title | Note |
|---|---|---|
| 2605.18747 | Code as Agent Harness | code-as-substrate survey (Ep 3, 8) |
| 2603.25723 | Natural-Language Agent Harnesses | Ep 1 |
| 2604.08224 | Externalization in LLM Agents | Ep 1 |
| 2605.09998 | Continual Harness: Online Adaptation | Ep 5 (related) |
| 2607.13683 | Self-Evolving Agent Harnesses (Gated Semantic QD) | Ep 5 (related work only — NOT the source for our demo's result) |
| 2603.13372 | The ARC of Progress: A Living Survey | Ep 6 |
| 2602.14690 | Harness Engineering for Agentic AI Coding Tools | Ep 1 |
| 2602.15384 | World-Model–Augmented Web Agents | Ep 8 |
| 2503.16416 | A Survey on Evaluation of LLM-based Agents | Ep 6 |

---

## 6. Benchmarks — pull live on recording day

- **SWE-bench** — https://www.swebench.com/ — **numbers move monthly; read the live
  leaderboard on camera, do not quote a memorized percentage.**
- **AgentBench** — arXiv 2308.03688 — multi-environment agent eval.
- **Kaggle ARC-AGI-3** — https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3 —
  Scale C; top ~1.86 (own scale, ~50% of test data). Stale fast; re-check live.

---

## 7. Frameworks (see `resources_2026.md` §4 for hedges)

- **Vercel AI SDK 7** (2026-06-25, GA; `HarnessAgent` is *experimental*) —
  https://vercel.com/blog/ai-sdk-7 · https://ai-sdk.dev/docs/ai-sdk-harnesses/overview
- **Mastra** (TS, 1.0 Jan 2026) — https://mastra.ai/ *(its benchmark claim is a memory
  result — a vendor claim on LongMemEval; never present it as a harness ranking)*
- **LangGraph** https://www.langchain.com/langgraph · **CrewAI** https://crewai.com/ ·
  **Strands** https://strandsagents.com/ · **Claude Agent SDK**
  https://code.claude.com/docs/en/agent-sdk/overview
- Landscape write-ups are **editorial, not benchmarked** — never present as a measured ranking.

---

## 8. The 2026 harness-effect literature (added 2026-09-12 — see `resources_2026.md` §7)

Additional evidence found after recording; used in show notes and errata.
Numbers exactly as `resources_2026.md` §7 has them.

- **Stop Comparing LLM Agents Without Disclosing the Harness** — arXiv 2605.23950 (2026-05-07), Zhang et al.: https://arxiv.org/abs/2605.23950 — ETCSOVG disclosure standard; 69.7 → 77.0 TB-2 (as reported from Lin et al. 2026).
- **Harness-Bench** — arXiv 2605.27922 (2026-05-27), Yao et al.: https://arxiv.org/abs/2605.27922 · code https://github.com/Qihoo360/harness-bench
- **Scaffold Effects on GAIA** — arXiv 2606.08529 (2026-06-07), Starace: https://arxiv.org/abs/2606.08529 — up to 28 pts within one model.
- **The Scaffold Effect in Coding Agents** — arXiv 2607.22585 (2026-06-08), Vats & Golev: https://arxiv.org/abs/2607.22585 — up to 40× tokens per solved task.
- **Does the Harness Matter?** — Agents' Last Exam blog (2026-06-11): https://agents-last-exam.org/blogs/harness-matters — model sweep 18 pts vs harness 5–6 pts.
- **From Question Answering to Task Completion** (survey) — arXiv 2606.20683 (2026-06-14), Guo et al.: https://arxiv.org/abs/2606.20683
- **Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents** — arXiv 2609.00006 (2026-07-15, CC BY 4.0), Barbaste et al.: https://arxiv.org/abs/2609.00006 — 29 patterns, 90-line MVH.
- **Niklaus, harness-optimization** (repo, 2026): https://github.com/JoelNiklaus/harness-optimization — Spearman −0.05 transfer; *repo-verified, not a paper*.
- **Artificial Analysis Coding Agent Index** methodology: https://artificialanalysis.ai/methodology/coding-agents-benchmarking
- Secondary / unverified (do not cite as fact): InfoQ on DeepSeek `dsh` (2026-08); agentconn.com 32× cost figure.
- **Refuted, do not cite:** the Inspect AI 0.3.12 "reliability score" (checked against PyPI 2026-09-12 — 0.3.12 is from 2024-05-31; current is 0.3.263).

---

## 9. Citation hygiene (standing rules)

- Verify arXiv IDs, titles, and author lists against the papers (`sources/` has local
  copies) — never cite from memory.
- No citation counts in on-screen citations — they decay and can't be verified live.
- Benchmark percentages that move (SWE-bench, Kaggle) are read live, never memorized.
- Third-party blog "guides" are not references; cite primary sources.
- Numbers not published by the benchmark's own organization are labeled **self-reported**.

---

**Last updated:** 2026-09-12 (§8 added; earlier sections verified 2026-07-18 / 2026-09-09) · **Authoritative claims file:** `resources_2026.md` ·
**Local PDFs:** `sources/`
