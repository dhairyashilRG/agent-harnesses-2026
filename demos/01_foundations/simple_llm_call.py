"""
Episode 1: a model with no harness.

Two questions. The model answers the first one well, because answering it needs nothing but
what is already in the weights. It cannot answer the second one at all, because the second
needs a fact from the world — and this program gives it no way to reach the world.

That gap is the entire series. Run `minimal_harness.py` next to watch the same model answer
the same question correctly, once it has a body.

    export OPENROUTER_API_KEY=sk-or-...
    python3 demos/01_foundations/simple_llm_call.py
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _llm import MODEL, EmptyReply, NoKey, text  # noqa: E402

# Reasoning models spend completion tokens thinking before they write anything.
# 200 was not enough for a two-sentence answer -- the budget ran out mid-thought
# and the reply came back empty. Give them room; see _llm.EmptyReply.
BUDGET = 1500


def main() -> int:
    try:
        print("=" * 68)
        print(f"DEMO: a model on its own   (model={MODEL})")
        print("=" * 68)

        print("\n[1] Something it can answer from what it already knows")
        print("-" * 68)
        answer = text(
            [{"role": "user",
              "content": "In two sentences, what makes a software architecture good?"}],
            max_tokens=BUDGET)
        print(answer)

        print("\n[2] Something that needs the world")
        print("-" * 68)
        answer = text(
            [{"role": "user",
              "content": "What is the current weather in San Francisco right now?"}],
            max_tokens=BUDGET)
        print(answer)

        print("\n" + "-" * 68)
        print("The model has no clock, no network and no memory of five minutes ago.")
        print("Whatever it said above about the weather, it did not check.")
        print("A harness is what closes that gap -> minimal_harness.py")
        print("=" * 68)
        return 0
    except NoKey as e:
        print(e)
        return 2
    except EmptyReply as e:
        # Loud, not silent -- the whole point of Episode 7's Card 1.
        print(f"\n[harness] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
