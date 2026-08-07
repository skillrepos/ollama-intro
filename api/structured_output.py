# structured_output.py - Force the model to answer with valid JSON that matches a schema.
# Lab 4 (optional) - Introduction to Ollama
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
        "used_for": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["name", "category", "used_for"],
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
            "options": {"temperature": 0},
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

    # Because we passed a schema, this parse should succeed every time.
    parsed = json.loads(raw)
    print("Parsed as a real Python object:")
    print(f"  name           = {parsed.get('name')}")
    print(f"  category       = {parsed.get('category')}")
    print(f"  first_released = {parsed.get('first_released')}")
    print(f"  used_for       = {', '.join(parsed.get('used_for', []))}")
