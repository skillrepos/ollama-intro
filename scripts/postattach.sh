#!/usr/bin/env bash
# Runs on every attach to the codespace.
#
# This is launched DETACHED (setsid + nohup) by postAttachCommand in
# .devcontainer/devcontainer.json. That is deliberate: VS Code lets extensions
# "relaunch the terminal to contribute to its environment" (Python, Python
# Debugger, Git), and that relaunch sends a Ctrl+C into the post-attach
# terminal. Anything still running in the foreground there gets killed.
# Detaching puts this in its own session so the Ctrl+C cannot reach it.
cd "$(dirname "$0")/.." || exit 0
bash scripts/startOllama.sh
