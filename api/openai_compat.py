# openai_compat.py - Point the official OpenAI SDK at your local Ollama server.
# Lab 6 - Introduction to Ollama
#
# Ollama exposes an OpenAI-compatible surface at http://localhost:11434/v1.
# That means most code written against OpenAI works unchanged - you only swap
# base_url and the model name. The api_key is required by the SDK but ignored
# by Ollama, so any non-empty string works.

import os
import sys

from openai import OpenAI

BASE_URL = os.environ.get("OLLAMA_HOST_URL", "http://localhost:11434") + "/v1"
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")

client = OpenAI(base_url=BASE_URL, api_key="ollama")


def main():
    prompt = " ".join(sys.argv[1:]) or "Name three tradeoffs of running an LLM locally."

    print(f"base_url = {BASE_URL}")
    print(f"model    = {MODEL}\n")

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are terse and concrete."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=200,
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
    print("\n")

    print("Same SDK, same call shape. Only base_url and model changed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nRequest failed: {e}")
        print("Is Ollama running? Try: bash scripts/startOllama.sh")
        sys.exit(1)
