"""
Episode 1: the same model, with a body.

`simple_llm_call.py` asked this model for the current weather and it correctly said it had
no way to find out. This file asks the identical question, of the identical model, and gets
a real answer — because here the model can call a real weather API.

Nothing about the model changed. What changed is about eighty lines of code around it.
That is the harness, and that is the entire thesis of the series.

Both tools are real:
  * weather   — live call to Open-Meteo (no API key, no signup)
  * calculator — the AST-allowlist calculator from demos/SAFE_CALCULATOR.py

    export OPENROUTER_API_KEY=sk-or-...
    python3 demos/01_foundations/minimal_harness.py
"""

import json
import os
import sys
from typing import Any, Dict, List

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _llm import MODEL, EmptyReply, NoKey, chat  # noqa: E402
from SAFE_CALCULATOR import SafeCalculator  # noqa: E402

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WX_URL = "https://api.open-meteo.com/v1/forecast"


# ------------------------------------------------------------------ the tools
def get_weather(city: str) -> str:
    """Real current conditions for a real place. No key required."""
    geo = requests.get(GEO_URL, params={"name": city, "count": 1}, timeout=30).json()
    if not geo.get("results"):
        return f"No place called {city!r} was found."
    place = geo["results"][0]
    wx = requests.get(WX_URL, params={
        "latitude": place["latitude"], "longitude": place["longitude"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto"}, timeout=30).json()
    now = wx["current"]
    return (f"{place['name']}, {place.get('country_code','')}: "
            f"{now['temperature_2m']}°C, humidity {now['relative_humidity_2m']}%, "
            f"wind {now['wind_speed_10m']} km/h (local time {now['time']})")


def calculate(expression: str) -> str:
    return str(SafeCalculator().evaluate(expression))


TOOLS = {"get_weather": get_weather, "calculate": calculate}

# What the model is told exists. It knows nothing about the world beyond this.
SCHEMA: List[Dict[str, Any]] = [
    {"type": "function", "function": {
        "name": "get_weather",
        "description": "Current weather for a city, live. Use for any question about "
                       "what the weather is right now.",
        "parameters": {"type": "object",
                       "properties": {"city": {"type": "string",
                                               "description": "City name, e.g. 'San Francisco'"}},
                       "required": ["city"]}}},
    {"type": "function", "function": {
        "name": "calculate",
        "description": "Evaluate an arithmetic expression, e.g. '15 * 23 + 100'.",
        "parameters": {"type": "object",
                       "properties": {"expression": {"type": "string"}},
                       "required": ["expression"]}}},
]


# ------------------------------------------------------------------ the loop
def run(task: str, max_steps: int = 6) -> str:
    """Think -> act -> observe, until the model stops asking for tools.

    The whole harness is this function. Note what it owns: the message list, the decision
    to execute a tool, how the result is phrased on the way back, and when to stop. The
    model owns exactly one thing — what to say next.
    """
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content":
         "You answer using the tools provided. Call a tool rather than guessing at "
         "anything you cannot know, then answer in one short sentence."},
        {"role": "user", "content": task},
    ]
    prompt_tokens = completion_tokens = 0

    for step in range(1, max_steps + 1):
        print(f"\n--- step {step} " + "-" * 52)
        result = chat(messages, tools=SCHEMA, max_tokens=2000)
        msg = result["message"]
        prompt_tokens += result["usage"].get("prompt_tokens", 0)
        completion_tokens += result["usage"].get("completion_tokens", 0)

        calls = msg.get("tool_calls") or []
        if not calls:
            answer = (msg.get("content") or "").strip()
            print(f"model answers: {answer}")
            print("-" * 62)
            print(f"tokens: {prompt_tokens} prompt + {completion_tokens} completion")
            return answer

        messages.append(msg)                      # the assistant's turn, verbatim
        for call in calls:
            name = call["function"]["name"]
            args = json.loads(call["function"]["arguments"] or "{}")
            print(f"model wants : {name}({', '.join(f'{k}={v!r}' for k, v in args.items())})")
            try:
                observation = TOOLS[name](**args)
            except Exception as e:                # a tool failing is normal, not fatal
                observation = f"tool error: {e}"
            print(f"tool returns: {observation}")
            # The tool_call_id must match, or the next call is rejected.
            messages.append({"role": "tool", "tool_call_id": call["id"],
                             "name": name, "content": observation})

    return "hit the step limit without a final answer"


def main() -> int:
    print("=" * 62)
    print(f"DEMO: the same model, with tools   (model={MODEL})")
    print("=" * 62)
    try:
        run("What is the weather in San Francisco right now, and what is "
            "that temperature in Fahrenheit?")
        print("\nSame model as simple_llm_call.py. The difference is the harness.")
        print("=" * 62)
        return 0
    except NoKey as e:
        print(e)
        return 2
    except EmptyReply as e:
        print(f"\n[harness] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
