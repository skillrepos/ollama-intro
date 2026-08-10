# rest_generate.py - Talk to Ollama's local REST API using nothing but 'requests'.
# Bonus example - Introduction to Ollama (not used in a lab; shows the API with bare requests)
#
# There is no Ollama library involved here on purpose. This is the raw HTTP
# contract that every Ollama client - Python, JavaScript, LangChain, curl -
# is built on top of.

import json
import os
import sys
import time

import requests

HOST = os.environ.get("OLLAMA_HOST_URL", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")


def list_models():
    """GET /api/tags - what is installed locally."""
    resp = requests.get(f"{HOST}/api/tags", timeout=30)
    resp.raise_for_status()
    print("Locally installed models:")
    for m in resp.json().get("models", []):
        size_gb = m.get("size", 0) / 1e9
        print(f"  {m['name']:<28} {size_gb:>5.1f} GB")
    print()


def generate_once(prompt):
    """POST /api/generate with stream=false - one request, one complete answer."""
    print(f"--- /api/generate (stream=false) with {MODEL} ---")
    start = time.time()
    resp = requests.post(
        f"{HOST}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.3, "num_predict": 80},
        },
        timeout=300,
    )
    resp.raise_for_status()
    data = resp.json()
    print(data["response"].strip())
    print(
        f"\n[done in {time.time() - start:.1f}s | "
        f"{data.get('eval_count', 0)} tokens generated]\n"
    )


def generate_streaming(prompt):
    """POST /api/generate with stream=true - newline-delimited JSON, token by token."""
    print(f"--- /api/generate (stream=true) with {MODEL} ---")
    with requests.post(
        f"{HOST}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": True,
            "options": {"temperature": 0.3, "num_predict": 80},
        },
        stream=True,
        timeout=300,
    ) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            print(chunk.get("response", ""), end="", flush=True)
            if chunk.get("done"):
                print("\n")
                break


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or "In two sentences, what is a container image?"

    try:
        list_models()
        generate_once(prompt)
        generate_streaming(prompt)
    except requests.exceptions.ConnectionError:
        print(f"Could not reach Ollama at {HOST}.")
        print("Is the service running? Try: bash scripts/startOllama.sh")
        sys.exit(1)
