"""
The provider boundary — one place the whole repo talks to a model.

Every demo calls `chat()`. Nothing else in the repo knows which provider is behind it,
which is the Episode 3 point made concrete: swapping the model should touch one file, and
the harness around it should not notice. It didn't used to be true here — five demos each
imported a vendor SDK directly, and changing provider meant editing five files and holding
two API keys.

Provider: OpenRouter (OpenAI-compatible chat completions), so any of its ~400 models works
by changing one env var.

    export OPENROUTER_API_KEY=sk-or-...
    # optional: export OPENROUTER_MODEL=<any openrouter model id>

Why `meta/muse-spark-1.3` and not the cheaper `...-1.3-contributor`: the contributor tier
is a third of the price because your prompts become training data, and it only serves once
you allow paid-endpoint training in OpenRouter's privacy settings. For a public repo that
strangers will run against their own keys, the default should not quietly opt them into
that. Set OPENROUTER_MODEL if you want the cheaper tier for your own runs.

Returns the raw assistant message dict plus usage, because a harness that can't see what a
call cost can't make it cheaper (Episode 4).
"""

import json
import os
from typing import Any, Dict, List, Optional

import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.getenv("OPENROUTER_MODEL", "meta/muse-spark-1.3")
TIMEOUT = 180


class NoKey(RuntimeError):
    """Raised with a fixable message rather than a stack trace in someone's face."""


class EmptyReply(RuntimeError):
    """The model returned 200 OK and no content.

    This is the failure mode Episode 7 calls Card 1 and Episode 4 calls the reasoning-model
    gotcha, and it is not hypothetical — it happens on every reasoning model here when the
    token budget is spent on thinking before any answer is emitted. Silence looks identical
    to success, so the harness must tell "the model said nothing" apart from "the model is
    done." That is why this raises instead of returning "".
    """


def api_key() -> str:
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise NoKey(
            "OPENROUTER_API_KEY is not set.\n"
            "  Get one at https://openrouter.ai/keys, then:\n"
            "    export OPENROUTER_API_KEY=sk-or-...\n"
            "  Offline demos need no key: python3 demos/run_all.py --offline"
        )
    return key


def chat(messages: List[Dict[str, Any]],
         tools: Optional[List[Dict]] = None,
         max_tokens: int = 4096,
         temperature: float = 0.0,
         model: Optional[str] = None) -> Dict[str, Any]:
    """One chat-completion round trip.

    Returns {"message": <assistant message dict>, "usage": {...}, "model": str}.
    The assistant message is passed straight back into `messages` on the next turn —
    including any `tool_calls` — so the caller owns the loop, not this function.
    """
    body: Dict[str, Any] = {
        "model": model or MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if tools:
        body["tools"] = tools
        body["tool_choice"] = "auto"

    r = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {api_key()}",
                 "Content-Type": "application/json"},
        json=body,
        timeout=TIMEOUT,
    )
    if r.status_code != 200:
        raise RuntimeError(f"OpenRouter {r.status_code}: {r.text[:400]}")
    data = r.json()
    if "choices" not in data:
        raise RuntimeError(f"unexpected response: {json.dumps(data)[:400]}")
    msg = data["choices"][0]["message"]
    usage = data.get("usage", {})

    # Reasoning models spend the completion budget thinking. If it runs out before any
    # answer is written you get 200 OK with content=None -- so check, and say why.
    if not msg.get("content") and not msg.get("tool_calls"):
        reasoning = usage.get("completion_tokens_details", {}).get("reasoning_tokens", 0)
        raise EmptyReply(
            f"{body['model']} returned no content.\n"
            f"  completion_tokens={usage.get('completion_tokens')} "
            f"of max_tokens={max_tokens}, of which reasoning_tokens={reasoning}.\n"
            "  The budget was spent thinking before it wrote anything. Raise max_tokens."
        )

    return {"message": msg, "usage": usage,
            "model": data.get("model", body["model"])}


def text(messages, **kw) -> str:
    """`chat()` when all you want is the words."""
    return (chat(messages, **kw)["message"].get("content") or "").strip()


def reasoning_of(result: Dict[str, Any]) -> int:
    """Reasoning tokens billed on a call — invisible in `content`, visible on the bill."""
    return (result.get("usage", {})
            .get("completion_tokens_details", {})
            .get("reasoning_tokens", 0))
