# warmup.py - Pre-load models into memory so lab prompts don't pay the load penalty.
# Lab 1 - Introduction to Ollama
#
# The slowest prompt you ever send to a model is the first one, because the
# weights have to be read from disk into RAM before a single token is produced.
# This script pays that cost up front, for every model we're about to use.
#
# It works by POSTing to /api/generate with a model but NO prompt. Ollama loads
# the model and returns immediately without generating anything. The keep_alive
# value then tells Ollama how long to hold it in memory.
#
# Usage:
#   python api/warmup.py                    # warm the two workshop models
#   python api/warmup.py shellcoach         # warm a model you just created
#   python api/warmup.py llama3.2:3b 60m    # warm one model, hold it for an hour

import re
import sys
import time

import requests

HOST = "http://localhost:11434"
DEFAULT_MODELS = ["llama3.2:3b", "llama3.2:1b"]
DEFAULT_KEEP_ALIVE = "-1"   # -1 = never unload (matches the server's OLLAMA_KEEP_ALIVE=-1)

# 30m, 1h, 90s, 0, -1 - but not "shellcoach"
DURATION = re.compile(r"-?\d+(?:\.\d+)?(?:ms|s|m|h)?")


def installed_models():
    """Everything currently on disk, so we can warn about typos before we wait."""
    try:
        resp = requests.get(f"{HOST}/api/tags", timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException:
        return None
    return {m["name"] for m in resp.json().get("models", [])}


def as_keep_alive(value):
    """Ollama accepts keep_alive as EITHER a duration string ("30m", "1h") OR a
    plain number of seconds, where -1 means "never unload". A bare number has to
    be sent as a JSON number: the string "-1" is parsed as a duration, has no unit
    suffix, and the API rejects the request with 400 Bad Request."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return value


def load(model, keep_alive):
    """Load one model into memory. No prompt means no generation - just the load."""
    start = time.time()
    resp = requests.post(
        f"{HOST}/api/generate",
        json={"model": model, "keep_alive": as_keep_alive(keep_alive)},
        timeout=600,
    )
    resp.raise_for_status()
    return time.time() - start


def loaded_now():
    """What /api/ps reports - the same thing 'ollama ps' prints."""
    resp = requests.get(f"{HOST}/api/ps", timeout=15)
    resp.raise_for_status()
    return resp.json().get("models", [])


def main():
    args = [a for a in sys.argv[1:]]

    # A trailing duration like 30m / 1h / 90s / -1 / 0 is treated as the keep_alive
    # value. It has to look like a real duration - a model name that happens to end
    # in 'h' (shellcoach) must not be mistaken for one.
    keep_alive = DEFAULT_KEEP_ALIVE
    if args and DURATION.fullmatch(args[-1]):
        keep_alive = args.pop()

    models = args or DEFAULT_MODELS

    print("=" * 58)
    print("Ollama warmup")
    print(f"  models     : {', '.join(models)}")
    label = "-1 (never unload)" if str(keep_alive) == "-1" else str(keep_alive)
    print(f"  keep_alive : {label}")
    print("=" * 58)
    print()

    have = installed_models()
    if have is None:
        print(f"Could not reach Ollama at {HOST}.")
        print("Start it with: bash scripts/startOllama.sh")
        return 1

    results = []
    for model in models:
        if model not in have and f"{model}:latest" not in have:
            print(f"  {model:<24} SKIPPED - not installed (try: ollama pull {model})")
            continue
        print(f"  {model:<24} loading ...", end="", flush=True)
        try:
            secs = load(model, keep_alive)
        except requests.exceptions.RequestException as e:
            print(f" FAILED ({e})")
            continue
        print(f" ready in {secs:5.1f}s")
        results.append((model, secs))

    print()
    running = loaded_now()
    if running:
        print("Currently loaded:")
        print(f"  {'MODEL':<24}{'SIZE':>10}   UNTIL")
        for m in running:
            gb = m.get("size", 0) / 1e9
            # A pinned model gets a far-future expiry; 'ollama ps' prints that as Forever.
            expires = m.get("expires_at", "?")
            until = "Forever" if expires[:4].isdigit() and int(expires[:4]) > 2100 else expires[:19]
            print(f"  {m['name']:<24}{gb:>8.1f} GB   {until}")
    else:
        print("Nothing is loaded - something went wrong.")

    print()
    if results:
        total = sum(s for _, s in results)
        print(f"Warmed {len(results)} model(s) in {total:.1f}s.")
        print("Those seconds are now NOT charged to your first lab prompt.")
    print()
    print("Re-run this any time a model has been idle and unloaded - for example")
    print("after you create your own model:  python api/warmup.py shellcoach")
    return 0


if __name__ == "__main__":
    sys.exit(main())
