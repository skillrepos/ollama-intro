# cloud_chat.py - Run a large model you could never fit in this codespace.
# Lab 6 (optional) - Introduction to Ollama
#
# Ollama Cloud hosts large models behind the SAME API you have been using.
# There are two ways in:
#
#   A) Signed in locally ('ollama signin'): pull a '-cloud' tagged model and it
#      routes through your local server. Your code does not change at all.
#
#   B) Direct to ollama.com with an API key from https://ollama.com/settings/keys
#      export OLLAMA_API_KEY=your_key_here
#
# This script uses (B) if OLLAMA_API_KEY is set, and otherwise falls back to (A).

import os
import sys

from ollama import Client

CLOUD_MODEL = os.environ.get("OLLAMA_CLOUD_MODEL", "gpt-oss:120b")
LOCAL_CLOUD_TAG = os.environ.get("OLLAMA_CLOUD_TAG", "gpt-oss:120b-cloud")
API_KEY = os.environ.get("OLLAMA_API_KEY")


def build_client():
    if API_KEY:
        print(f"Using ollama.com directly with an API key -> {CLOUD_MODEL}\n")
        return (
            Client(
                host="https://ollama.com",
                headers={"Authorization": f"Bearer {API_KEY}"},
            ),
            CLOUD_MODEL,
        )

    print(f"No OLLAMA_API_KEY set. Routing through the local server -> {LOCAL_CLOUD_TAG}")
    print("(This requires 'ollama signin' and 'ollama pull " + LOCAL_CLOUD_TAG + "')\n")
    return Client(host="http://localhost:11434"), LOCAL_CLOUD_TAG


def main():
    prompt = " ".join(sys.argv[1:]) or (
        "Explain the difference between quantization and distillation in 4 sentences."
    )

    client, model = build_client()

    for chunk in client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    ):
        print(chunk["message"]["content"], end="", flush=True)
    print("\n")

    print("Notice: identical call shape to chat_app.py. Only the client and model changed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nRequest failed: {e}")
        print("\nChecklist:")
        print("  - Signed in?           ollama signin")
        print("  - Cloud model pulled?  ollama pull " + LOCAL_CLOUD_TAG)
        print("  - Or set a key:        export OLLAMA_API_KEY=...")
        print("  - Model names change. See https://ollama.com/search?c=cloud")
        sys.exit(1)
