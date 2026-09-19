"""
Central config for all demos. One place to change models and env-var names on
recording day, instead of editing every file.

Override with environment variables:
    DEEPSEEK_MODEL    (default: deepseek-flash — the current id; the older
                       "deepseek-v4-flash" still routes here but is legacy)
    DEEPSEEK_API_KEY  (required by DeepSeek demos; legacy name DEEPSEEK_API_PATAPI
                       is still honored so older shells keep working)

Most demos now go through demos/_llm.py (OpenRouter) and read OPENROUTER_MODEL —
this file is only for the two DeepSeek demos that call that API directly.

Recording-day note: confirm the model ids before the take, model names move.
"""

import os
from typing import Optional

DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-flash")


def deepseek_key() -> Optional[str]:
    """DeepSeek key, honoring the legacy env-var name."""
    return os.getenv("DEEPSEEK_API_KEY") or os.getenv("DEEPSEEK_API_PATAPI")
