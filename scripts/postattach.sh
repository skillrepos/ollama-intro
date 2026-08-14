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

# The Merge Info extension must be installed HERE, not in postCreateCommand.
# At postCreate time the VS Code server does not exist yet, so `code
# --install-extension` runs, reports nothing, and installs nothing - and the
# `|| true` hides it. By attach time the server is up and the install works.
code --install-extension "$PWD/.devcontainer/merge-info-0.1.0.vsix" --force > /tmp/merge-info-install.log 2>&1 || true

bash scripts/startOllama.sh
