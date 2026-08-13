#!/usr/bin/env bash
# startup_ollama.sh - bring Ollama up at codespace creation time.
#
# With the prebuilt image this is nearly a no-op: the binary is already
# installed and both workshop models are already in /opt/ollama-models. All
# that is left is starting the server and warming the default model.
#
# Every install/pull below is CONDITIONAL so that this script still works on a
# plain base image (a fork, or a local Dev Container build). Do not make any of
# them unconditional - that would re-download things the image already has.

MODEL="${OLLAMA_MODEL:-llama3.2:3b}"

echo "========================================"
echo "Ollama startup"
echo "Lab model: $MODEL"
echo "========================================"
echo ""

# --- Ollama binary -----------------------------------------------------------
if command -v ollama > /dev/null 2>&1; then
    echo "Ollama already installed (baked into the image)."
else
    echo "Installing Ollama..."
    # The installer extracts a zstd tarball; the stock base image lacks zstd.
    command -v zstd > /dev/null 2>&1 || \
        (sudo apt-get update -qq && sudo apt-get install -y -qq zstd)
    curl -fsSL https://ollama.com/install.sh | sh
    if ! command -v ollama > /dev/null 2>&1; then
        echo "  ERROR: Ollama install failed - nothing below will work."
        exit 1
    fi
fi
echo ""

# --- Server ------------------------------------------------------------------
if curl -sS http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Ollama service already running."
else
    echo "Starting Ollama..."
    export OLLAMA_KEEP_ALIVE=-1
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    ATTEMPTS=0
    until curl -sS http://localhost:11434/api/tags > /dev/null 2>&1; do
        ATTEMPTS=$((ATTEMPTS+1))
        if [ $ATTEMPTS -gt 60 ]; then
            echo "  ERROR: Ollama did not become ready. See /tmp/ollama.log"
            exit 1
        fi
        sleep 1
    done
    echo "  ready (log: /tmp/ollama.log)"
fi
echo ""

# --- Models ------------------------------------------------------------------
# Only the default model. llama3.2:1b is intentionally left out: students pull
# it themselves in Lab 1 step 2. Adding it here would make that step a no-op.
for m in "$MODEL"; do
    if ollama list 2>/dev/null | grep -q "^${m%%:*}[[:space:]]*${m##*:}\|^${m}[[:space:]]"; then
        echo "  $m already present"
    else
        echo "  Pulling $m (not in the image) ..."
        ollama pull "$m"
    fi
done
echo ""

# --- Warm the default model so the first lab prompt is not the slow one ------
echo "Warming $MODEL ..."
curl -sS -X POST http://localhost:11434/api/generate \
     -d "{\"model\": \"$MODEL\", \"keep_alive\": -1}" > /dev/null
echo ""

echo "========================================"
ollama list
echo ""
echo "Ollama API endpoint: http://localhost:11434"
echo "Ready for lab exercises!"
echo "========================================"
