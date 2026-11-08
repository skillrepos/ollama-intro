# structured_output.py - Force the model to answer with valid JSON that matches a schema.
# Lab 5 - Introduction to Ollama
#
# This is the single most useful API feature for real applications: instead of
# parsing prose with regexes, you hand Ollama a JSON Schema in the "format"
# field and get back something you can json.loads() with confidence.

import json
import os
import sys

import requests

HOST = os.environ.get("OLLAMA_HOST_URL", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")

SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "category": {
            "type": "string",
            "enum": ["language", "database", "framework", "tool", "other"],
        },
        "first_released": {"type": "integer"},
        # maxItems keeps the list short. Without a limit, a small model can
        # keep adding items and never close the list.
        "used_for": {"type": "array", "items": {"type": "string"}, "maxItems": 4},
    },
    "required": ["name", "category", "first_released", "used_for"],
}


def describe(thing):
    resp = requests.post(
        f"{HOST}/api/chat",
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": f"Describe '{thing}' as a JSON object.",
                }
            ],
            "format": SCHEMA,
            "stream": False,
            # num_predict is a safety net, as in Lab 1: a hard stop on answer length.
            "options": {"temperature": 0, "num_predict": 300},
        },
        timeout=300,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


if __name__ == "__main__":
    thing = " ".join(sys.argv[1:]) or "PostgreSQL"

    try:
        raw = describe(thing)
    except requests.exceptions.ConnectionError:
        print(f"Could not reach Ollama at {HOST}. Try: bash scripts/startOllama.sh")
        sys.exit(1)

    print("Raw response from the model:")
    print(raw)
    print()

    # Because we passed a schema, this parse should succeed. It can only fail
    # if num_predict cut the answer off before the JSON was finished.
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        print("The answer was cut off before the JSON was complete (num_predict reached).")
        sys.exit(1)
    print("Parsed as a real Python object:")
    # Driven off the parsed dict rather than a hard-coded field list, so that if
    # you add a property to SCHEMA (Lab 5 step 4) it shows up here too.
    for key, value in parsed.items():
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        print(f"  {key:<14} = {value}")
