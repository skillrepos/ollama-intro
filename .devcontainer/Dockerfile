# Prebuilt dev container for the "Getting Started with Ollama" workshop.
#
# Everything here used to happen at codespace-creation time, in front of the
# student. Baking it into the image moves that cost to a build you run once.
# See IMAGEMAINTENANCE.md for when and how to rebuild.
#
# Build from the REPO ROOT (the COPY below needs requirements.txt):
#   docker build --platform linux/amd64 -f .devcontainer/Dockerfile \
#     -t ghcr.io/skillrepos/ollama-intro-devcontainer:latest .

FROM mcr.microsoft.com/devcontainers/base:bookworm

# ---------------------------------------------------------------------------
# 1. OS packages
#    zstd is not optional: the Ollama installer extracts a zstd-compressed
#    tarball, and the base image does not ship it. Without zstd the install
#    dies with "ERROR: This version requires zstd for extraction".
# ---------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        zstd curl ca-certificates python3 python3-venv python3-pip && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# 2. Node LTS
#    Present for exactly one reason: Claude Code in Lab 4 step 9. Replaces the
#    devcontainer "node" feature.
# ---------------------------------------------------------------------------
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# 3. Claude Code - launched by `ollama launch claude` in Lab 4 step 9
# ---------------------------------------------------------------------------
RUN npm install -g @anthropic-ai/claude-code && \
    npm cache clean --force

# ---------------------------------------------------------------------------
# 4. Python virtualenv, prebuilt at /opt/py_env
#    scripts/pysetup.sh copies this into the workspace and rewrites the paths.
#    No pip download happens at startup.
# ---------------------------------------------------------------------------
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m venv /opt/py_env && \
    /opt/py_env/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/py_env/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    find /opt/py_env -type d -name tests -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/py_env -name '*.pyc' -delete 2>/dev/null || true

# ---------------------------------------------------------------------------
# 5. Ollama binary, minus the GPU runtimes
#    Codespaces has no GPU, and the CUDA/Vulkan runtimes are several GB of the
#    install. Deleting them in the SAME layer is what actually shrinks the
#    image - a separate RUN would leave them in the layer below.
# ---------------------------------------------------------------------------
RUN curl -fsSL https://ollama.com/install.sh | sh && \
    rm -rf /usr/local/lib/ollama/cuda_v12 \
           /usr/local/lib/ollama/cuda_v13 \
           /usr/local/lib/ollama/mlx_cuda_v13 \
           /usr/local/lib/ollama/vulkan

# ---------------------------------------------------------------------------
# 6. The workshop models, baked in
#    This is the single biggest saving: ~3.3 GB that every student currently
#    downloads at creation time. `ollama pull` needs a running server, so the
#    server is started and stopped inside this one layer.
#
#    OLLAMA_MODELS points the store at /opt so it survives as an image layer -
#    the default ~/.ollama would land in the user's home.
# ---------------------------------------------------------------------------
ENV OLLAMA_MODELS=/opt/ollama-models
RUN mkdir -p /opt/ollama-models; \
    ollama serve > /tmp/build-ollama.log 2>&1 & \
    OLLAMA_PID=$!; \
    for i in $(seq 1 60); do \
        if curl -sf http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then break; fi; \
        sleep 1; \
    done; \
    ollama pull llama3.2:3b && \
    ollama list; \
    STATUS=$?; \
    kill "$OLLAMA_PID" 2>/dev/null || true; \
    exit $STATUS

# Students build their own model in Lab 2 (`ollama create shellcoach`) and pull
# a cloud tag in Lab 4, so the store has to be writable by the codespace user.
RUN chown -R vscode:vscode /opt/ollama-models /opt/py_env

# Keep models resident for the life of the codespace. The default is 5 minutes,
# which makes the first prompt after any pause pay a silent reload cost.
ENV OLLAMA_KEEP_ALIVE=-1
