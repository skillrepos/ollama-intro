#!/bin/bash
# startOllama.sh - Re-attach helper. Runs every time you reconnect to the codespace.
# Makes sure the Ollama service is running without re-pulling models.

if ! command -v ollama &> /dev/null; then
    # zstd is required by the Ollama installer and is absent from the base image.
    if ! command -v zstd &> /dev/null; then
        sudo apt-get update -qq && sudo apt-get install -y -qq zstd
    fi
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Never report success if the install did not actually land.
if ! command -v ollama &> /dev/null; then
    echo "ERROR: Ollama is not installed and could not be installed automatically."
    echo "Try:  sudo apt-get install -y zstd && curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Ollama is already running on http://localhost:11434"
else
    echo "Starting Ollama..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    echo "Ollama started. Log file: /tmp/ollama.log"
fi

# Pre-load the workshop models so the first lab prompt is not the slow one.
# Runs in the background - it does not hold up your terminal.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -x "$REPO_ROOT/py_env/bin/python" ]; then
    echo "Warming up models in the background (see /tmp/warmup.log)..."
    nohup "$REPO_ROOT/py_env/bin/python" "$REPO_ROOT/api/warmup.py" > /tmp/warmup.log 2>&1 &
fi
