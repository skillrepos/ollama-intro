#!/bin/bash
# startup_ollama.sh - Install Ollama, start the service, and pre-pull/warm the lab model.
# Run once at codespace creation time (postCreateCommand).

MODEL="${OLLAMA_MODEL:-llama3.2:3b}"

echo "========================================"
echo "Ollama Startup & Warmup Script"
echo "Lab model: $MODEL"
echo "========================================"
echo ""

# Step 1: Check and install Ollama if needed
echo "Step 1: Checking for Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "  Ollama is already installed"
else
    echo "  Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo "  Ollama installed"
fi
echo ""

# Step 2: Start the Ollama service
echo "Step 2: Starting Ollama service..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "  Ollama service already running"
else
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    echo "  Ollama started (log: /tmp/ollama.log)"
fi
echo ""

# Step 3: Wait for the service to answer
echo "Step 3: Waiting for Ollama to be ready..."
sleep 3
ATTEMPTS=0
until curl -s http://localhost:11434/api/tags > /dev/null 2>&1; do
    ATTEMPTS=$((ATTEMPTS+1))
    if [ $ATTEMPTS -gt 60 ]; then
        echo "  ERROR: Ollama did not become ready. See /tmp/ollama.log"
        exit 1
    fi
    echo "  Waiting for Ollama server..."
    sleep 1
done
echo "  Ollama server is ready"
echo ""

# Step 4: Pull the lab models
echo "Step 4: Pulling lab models (this may take several minutes)..."
for m in "$MODEL" "llama3.2:1b"; do
    if ollama list | grep -q "${m%%:*}.*${m##*:}"; then
        echo "  $m already present"
    else
        echo "  Pulling $m ..."
        ollama pull "$m"
    fi
done
echo ""

# Step 5: Warm up the primary model so the first lab prompt is not the slow one
echo "Step 5: Warming up $MODEL ..."
curl -s -X POST http://localhost:11434/api/generate -d "{
  \"model\": \"$MODEL\",
  \"prompt\": \"Hello\",
  \"stream\": false
}" > /dev/null
echo "  Model warmed up and ready"
echo ""

# Step 6: Status
echo "========================================"
echo "Status: Ollama Ready for Labs"
echo "========================================"
echo ""
echo "Installed models:"
ollama list
echo ""
echo "Ollama API endpoint: http://localhost:11434"
echo ""
echo "Ready for lab exercises!"
echo "========================================"
