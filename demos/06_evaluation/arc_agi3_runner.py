"""
ARC-AGI-3 scoring — real RHAE implementation.

Every number here is from a primary source, checked 2026-07-17/18 and re-checked 2026-09-09. Sources are cited
inline. The RHAE formula is implemented from the published spec, so the numbers this
prints are computed rather than hardcoded.

  Methodology : https://docs.arcprize.org/methodology
  Human study : https://arcprize.org/blog/arc-agi-3-human-dataset
  Milestone 1 : https://arcprize.org/blog/arc-prize-2026-milestone-1
  Duck harness: https://tufalabs.ai/research/duck-harness/
  ARC analysis: https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis
  EWM paper   : https://arxiv.org/abs/2605.05138
"""

from dataclasses import dataclass
from typing import List, Optional


# --- RHAE, per docs.arcprize.org/methodology -------------------------------

LEVEL_CAP = 1.15  # an agent beating the human baseline caps at 115% on a level


def level_score(human_baseline_actions: int, ai_actions: int) -> float:
    """Score one level.

    level_score = min(1.15, (human_baseline / ai_actions) ** 2)

    The square is the whole point: 2x the actions is 1/4 the score, 10x is
    ~1/100. Brute-force exploration is punished, not just slowed down.
    """
    if ai_actions <= 0:
        raise ValueError("ai_actions must be positive")
    return min(LEVEL_CAP, (human_baseline_actions / ai_actions) ** 2)


def game_score(level_scores: List[Optional[float]], total_levels: int) -> float:
    """Weighted average over levels, weight = 1-indexed level number.

    Later levels count more, so tutorial levels can't carry the score. Levels the
    agent never finished contribute 0 but still count in the denominator, which is
    what caps an incomplete run: finishing 4 of 5 levels ceilings you at
    (1+2+3+4)/(1+2+3+4+5) = 66.7% no matter how efficient you were.
    """
    weighted = sum(
        (i + 1) * s
        for i, s in enumerate(level_scores)
        if s is not None
    )
    denominator = sum(range(1, total_levels + 1))
    return weighted / denominator


def benchmark_score(game_scores: List[float]) -> float:
    """Final score = plain average of game scores. Scale is 0-1 (reported 0-100%)."""
    return sum(game_scores) / len(game_scores) if game_scores else 0.0


# --- Verified published results --------------------------------------------

@dataclass
class Result:
    system: str
    score: str
    metric: str
    source: str
    verified: bool


# Scale A — the OFFICIAL leaderboard, semi-private dataset. Re-checked against
# arcprize.org/results and arcprize.org/blog/astra on 2026-09-09. Four months moved
# this table from "nobody can touch it" to "essentially solved", so every row carries
# its own date — read the date before you read the score.
LEADERBOARD = [
    Result("GPT-6 Astra (provider adapter harness)", "99.9%  (2026-09-02)",
           "semi-private set; $19K; ARC Prize's own two-harness evaluation",
           "arcprize.org/blog/astra", True),
    Result("GPT-6 Astra (standard harness)", "62.7%  (2026-09-02)",
           "semi-private set; $26K; SAME MODEL, SAME DAY — only the harness differs",
           "arcprize.org/blog/astra", True),
    Result("Claude Opus 5", "30.16% (2026-07-24)", "semi-private set, standard harness",
           "arcprize.org/results", True),
    Result("GPT-5.6", "7.78%  (2026-07-09)", "semi-private set, standard harness",
           "arcprize.org/results", True),
    Result("Grok 4.6", "2.11%  (2026-08-11)", "semi-private set, standard harness",
           "arcprize.org/results", True),
    Result("GPT-5.5", "0.43%  (2026-05-01)", "semi-private set, standard harness",
           "arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis", True),
    Result("Opus 4.7", "0.18%  (2026-05-01)", "semi-private set, standard harness",
           "arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis", True),
    # 1.21% is Tufa's OWN reported number (X post), not published on an ARC Prize page:
    # the Milestone-1 blog states no scores, and the analysis page does not list Duck.
    # Marked verified=False for that reason (re-checked 2026-07-18).
    Result("Tufa Labs 'Duck'", "1.21%  (2026-07, self-reported)", "Milestone 1 winner; Tufa's own report, not an ARC Prize page",
           "x.com/tufalabs/status/2072336849465417747", False),
]

# Scale B — the PUBLIC 25-game set. Self-reported and hill-climbable: teams can
# iterate against these games directly, so the numbers run 30-50x higher than the
# leaderboard. Not comparable to Scale A.
PUBLIC_SET = [
    Result("Executable World Models + GPT-5.5 high", "58.12%", "public 25-game set, 15/25 solved",
           "arxiv.org/abs/2605.05138", True),
    Result("Executable World Models + GPT-5.4 high", "41.29%", "public 25-game set, 8/25 solved",
           "arxiv.org/abs/2605.05138", True),
    Result("Symbolica Agentica", "36.08%", "public 25-game set; author says unverified",
           "symbolica.ai/blog/arc-agi-3", False),
    Result("Tufa Labs 'Duck'", "1.6002 +/- 0.4475", "public games; UNITS NOT STATED in source",
           "tufalabs.ai/research/duck-harness/", False),
]

HUMAN_BASELINE_NOTE = (
    "Humans score ~100% by construction: the baseline IS the median first-time "
    "player per level, from a 458-participant study in San Francisco. "
    "(arcprize.org/blog/arc-agi-3-human-dataset)"
)


def demo_rhae_math():
    """Show RHAE behaviour with computed numbers."""
    print("=" * 72)
    print("RHAE — computed from the published formula")
    print("=" * 72)
    print("  level_score = min(1.15, (human_actions / ai_actions) ** 2)")
    print()

    human = 20
    print(f"Human baseline for this level: {human} actions")
    print()
    print(f"  {'AI actions':<12} {'ratio':<10} {'level score':<12} note")
    for ai_actions, note in [
        (17, "beats human, hits the 1.15 cap"),
        (20, "matches the median human"),
        (40, "2x actions -> quarter score"),
        (200, "10x actions -> near zero"),
    ]:
        s = level_score(human, ai_actions)
        print(f"  {ai_actions:<12} {human/ai_actions:<10.2f} {s:<12.4f} {note}")
    print()
    print("  This is why brute force scores ~0 even when it eventually wins.")
    print()


def demo_incomplete_game_ceiling():
    """Show how unfinished levels cap a game, with computed numbers."""
    print("=" * 72)
    print("Why finishing matters more than efficiency")
    print("=" * 72)

    total_levels = 5
    # Perfectly efficient on the first 4 levels, never finished level 5.
    scores = [1.0, 1.0, 1.0, 1.0, None]
    got = game_score(scores, total_levels)
    ceiling = sum(range(1, 5)) / sum(range(1, total_levels + 1))

    print(f"  Human-efficiency on levels 1-4, level 5 unfinished:")
    print(f"    game score = {got:.4f}  ({got*100:.1f}%)")
    print(f"    ceiling    = {ceiling:.4f}  ({ceiling*100:.1f}%)")
    print()
    print("  Perfect efficiency still caps at 66.7% with one level unfinished,")
    print("  because level weight = level number and the denominator counts all 5.")
    print()


def _print_table(title: str, rows: List[Result]):
    print(f"  {title}")
    print(f"  {'System':<40} {'Score':<20} {'Verified'}")
    print("  " + "-" * 70)
    for r in rows:
        flag = "yes" if r.verified else "NO"
        print(f"  {r.system:<40} {r.score:<20} {flag}")
    print()
    for r in rows:
        print(f"    {r.system}")
        print(f"      {r.metric}")
        print(f"      {r.source}")
    print()


def demo_published_results():
    print("=" * 72)
    print("Published results (quoted, as of 2026-09-09)")
    print("=" * 72)
    print()
    _print_table("SCALE A - official leaderboard (semi-private set) - read the date on each row",
                 LEADERBOARD)
    _print_table("SCALE B - public 25-game set (self-reported, hill-climbable)",
                 PUBLIC_SET)
    print("  SCALE C - Kaggle public leaderboard: ~1.86 top (YUTO KOJIMA), its own")
    print("            scale on ~50% of test data. Final standings will differ.")
    print()
    print(f"  {HUMAN_BASELINE_NOTE}")
    print()


def explain_scale_confusion():
    """The trap. Read this before building any chart from the tables above."""
    print("=" * 72)
    print("Do not put these numbers in one bar chart")
    print("=" * 72)
    print()
    print("  In July, Scale A topped out near 1.2% and Scale B reached 58.12% -")
    print("  the same benchmark and the same metric name, 48x apart.")
    print("  In September, Scale A reads 99.9%. The scales are still not")
    print("  comparable; only the direction of the error changed.")
    print()
    print("  The gap is not an error - it IS the lesson. Public games can be")
    print("  iterated against; the semi-private set cannot. A high public score")
    print("  is a hypothesis, not a result.")
    print()
    print("  The Executable World Models paper says this about its own 58.12%,")
    print("  which is a model of honest reporting (arxiv.org/abs/2605.05138):")
    print()
    print('    "Performance on the private validation set, which is not yet')
    print('     available to us, remains to be tested."')
    print('    "The private validation set is the decisive test of whether the')
    print('     current ARC-AGI-3-specific tools are genuinely game-general."')
    print()
    print("  OPEN QUESTION - do not assert either way. Duck reports a mean public")
    print("  game score of 1.6002 +/- 0.4475 and NEVER STATES THE UNITS - it is")
    print("  not called a percentage or an RHAE figure. One plausible reading,")
    print("  consistent with its 1.21% leaderboard score and the post's 'some")
    print("  games being solved consistently for over 40% of the levels', is that")
    print("  Duck solves levels but inefficiently, and RHAE's squared penalty")
    print("  crushes the score. That is INFERENCE, NOT CITATION. On camera, say")
    print("  the units are unstated and move on.")
    print()
    print("  Honest framing for the episode: Duck's 1.21% was near the top of the")
    print("  field in July and is a historical marker by September. Its story is")
    print("  cost and")
    print("  design, not score - Qwen 3.6 27B FP8, a Python REPL, image perception,")
    print("  context eviction, and 'an order of magnitude cheaper on each game'")
    print("  than the EWM agent using GPT-5.4 - which itself needed a $200/month")
    print("  ChatGPT Pro subscription to run 'roughly two to eight games'.")
    print()
    print("  Tufa's own position, worth quoting verbatim on camera:")
    print('    "solvability of a game being dependent on model capability, while')
    print('     the cost is mostly dictated by the harness."')
    print("  (tufalabs.ai/research/duck-harness/)")
    print()


if __name__ == "__main__":
    demo_rhae_math()
    demo_incomplete_game_ceiling()
    demo_published_results()
    explain_scale_confusion()
