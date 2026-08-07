#!/bin/bash
# shutdown_ollama.sh - Stop any loaded models and the Ollama service.
# Useful for troubleshooting ("address already in use") or freeing memory.

echo "Unloading any running models..."
ollama ps --format json 2>/dev/null | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | while read -r m; do
    [ -n "$m" ] && ollama stop "$m"
done

echo "Stopping the Ollama service..."
pkill ollama 2>/dev/null && echo "  Ollama stopped" || echo "  Ollama was not running"
