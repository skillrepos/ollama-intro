#!/usr/bin/env bash
# pysetup.sh - put the Python virtual environment in the workspace.
#
# FAST PATH: the prebuilt image ships a ready-made venv at /opt/py_env. We copy
# it into the workspace and rewrite the absolute paths inside it. No network,
# no pip, a couple of seconds.
#
# FALLBACK: no /opt/py_env (a plain base image, or a fork building without the
# prebuilt image), so create the venv and install requirements the slow way.
#
# The pip install MUST stay inside the else branch. If it runs unconditionally
# after the copy, every codespace re-downloads packages that are already in the
# image - which defeats the entire point of prebuilding.

PYTHON_ENV=${1:-py_env}
TARGET="$(pwd)/$PYTHON_ENV"

if [ -d "/opt/py_env" ] && [ ! -d "$TARGET" ]; then
    echo "Using the prebuilt virtual environment from the image..."
    cp -a /opt/py_env "$TARGET"
    # The venv records its own build-time path in several files; repoint them.
    sed -i "s|/opt/py_env|$TARGET|g" "$TARGET/bin/activate" 2>/dev/null || true
    sed -i "s|/opt/py_env|$TARGET|g" "$TARGET"/bin/pip* 2>/dev/null || true
    sed -i "s|/opt/py_env|$TARGET|g" "$TARGET/pyvenv.cfg" 2>/dev/null || true
    for f in "$TARGET"/bin/*; do
        head -c 2 "$f" 2>/dev/null | grep -q '#!' && \
            sed -i "1s|/opt/py_env|$TARGET|" "$f" 2>/dev/null || true
    done
    echo "  ready - no packages downloaded"
else
    if [ -d "$TARGET" ]; then
        echo "$PYTHON_ENV already exists - leaving it alone."
    else
        echo "No prebuilt environment found; building one (this takes a few minutes)..."
        python3 -m venv "$TARGET"
        if [ -f "./requirements.txt" ]; then
            "$TARGET/bin/pip" install -r "./requirements.txt"
        elif [ -f "./requirements/requirements.txt" ]; then
            "$TARGET/bin/pip" install -r "./requirements/requirements.txt"
        fi
    fi
fi

# Auto-activate in new shells (idempotent - do not append twice).
grep -qxF "source $TARGET/bin/activate" ~/.bashrc 2>/dev/null || \
    echo "source $TARGET/bin/activate" >> ~/.bashrc
