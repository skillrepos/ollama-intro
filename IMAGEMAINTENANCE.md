# Dev Container Image Maintenance

The Codespaces dev container uses a pre-built Docker image on GitHub Container
Registry (GHCR) so students do not wait through package installs and multi-GB
model pulls at startup. When certain files change, the image must be rebuilt
and pushed.

## Image location

```
ghcr.io/skillrepos/ollama-intro-devcontainer:latest
```

## What's baked into the image

| Component | How it got there | Why it matters |
|---|---|---|
| zstd, curl, ca-certificates, python3 | `apt-get install` | zstd is required by the Ollama installer |
| Node LTS | NodeSource apt repo | Needed only for Claude Code |
| Claude Code | `npm install -g @anthropic-ai/claude-code` | Lab 4 step 9 launches it |
| `/opt/py_env` (full virtualenv) | `pip install -r requirements.txt` | No pip download at startup |
| Ollama binary | `ollama.com/install.sh`, GPU runtimes deleted | Codespaces is CPU-only |
| **llama3.2:3b** (default model only) | `ollama pull` at build time, into `/opt/ollama-models` | ~2 GB no student downloads |

At startup, `scripts/pysetup.sh` copies `/opt/py_env` into the workspace and
rewrites its paths; `scripts/startup_ollama.sh` starts the server and warms the
default model. Neither needs the network.

## What is deliberately NOT in the image

- **llama3.2:1b.** Deliberately not baked. Students pull it in Lab 1 step 2,
  which is the only place the course teaches `ollama pull`. If you ever add it
  to the Dockerfile - or to the pull loop in `scripts/startup_ollama.sh` - that
  lab step silently becomes a no-op.
- **The Merge Info VS Code extension.** Extensions install into the VS Code
  server directory, which is not part of the container image. It stays in
  `postCreateCommand`.
- **docker-from-docker and github-cli features.** Removed entirely - nothing in
  the labs, README, or scripts uses `docker` or `gh`, and each feature added
  minutes to every student's container build.

## When to rebuild

| File changed | Rebuild needed? |
|---|---|
| `.devcontainer/Dockerfile` | **Yes** |
| `requirements.txt` | **Yes** - packages are pre-installed in `/opt/py_env` |
| The model list (in the Dockerfile) | **Yes** - models are baked in |
| `.devcontainer/devcontainer.json` | No - read at codespace creation |
| `scripts/*.sh` | No - they run at startup |
| `labs.md`, `api/*.py`, images, docs | No |

## How to rebuild and push

Run from the **repo root** - the `COPY requirements.txt` needs the repo root as
build context.

**You must pass `--platform linux/amd64`.** Codespaces runs on amd64; building
on Apple Silicon without this produces an arm64 image and Codespaces fails with
"No manifest found".

```bash
# 1. Log in to GHCR (one-time, or when the token expires)
docker login ghcr.io -u YOUR_GITHUB_USERNAME

# 2. Build (this pulls the models, so expect 10-20 minutes and ~7 GB)
docker build --platform linux/amd64 \
  -f .devcontainer/Dockerfile \
  -t ghcr.io/skillrepos/ollama-intro-devcontainer:latest .

# 3. Push
docker push ghcr.io/skillrepos/ollama-intro-devcontainer:latest
```

Then commit and push the repo changes so code and image stay in sync.

### Pinning a version

`:latest` means a rebuild silently changes what running codespaces get. For a
workshop you are about to deliver, tag and pin:

```bash
docker build --platform linux/amd64 -f .devcontainer/Dockerfile \
  -t ghcr.io/skillrepos/ollama-intro-devcontainer:2026-08 .
docker push ghcr.io/skillrepos/ollama-intro-devcontainer:2026-08
```

then set that tag in `devcontainer.json`. Rebuild `:latest` freely afterward
without touching the class you are teaching.

## Image size

Free Codespaces have a 32 GB storage limit, shared with Codespaces overhead
(agent, VS Code server, mounts). Rough budget for this image:

| Layer | Approx. |
|---|---|
| Base bookworm + apt packages | ~1.5 GB |
| Node + Claude Code | ~0.3 GB |
| `/opt/py_env` | ~0.2 GB |
| Ollama binary (GPU runtimes removed) | ~1.5 GB |
| Default model (llama3.2:3b) | ~2.0 GB |
| **Total** | **~5.5 GB** |

Keeping it that way:

- **Delete the GPU runtimes in the same `RUN` as the Ollama install.** A
  separate `RUN` leaves them in the layer below and the image stays large.
- **Do not add torch or sentence-transformers.** This course does not need
  them; they are what made the AI-AIP image tight.
- If a model is added, check the total - each 3B model is roughly 2 GB.

## Model store location

Models live at `/opt/ollama-models`, set by `OLLAMA_MODELS` in both the
Dockerfile and `devcontainer.json`. The default (`~/.ollama`) is not used,
because the store has to be an image layer.

The directory is `chown`ed to `vscode` at build time. That is required, not
cosmetic: students run `ollama create shellcoach` in Lab 2 and `ollama pull` a
cloud tag in Lab 4, both of which write here. If a rebuild ever drops that
`chown`, those steps fail with a permissions error.

## GHCR package visibility

Codespaces must be able to pull the image.

**Option A - make the package public.** Go to
`github.com/orgs/skillrepos/packages/container/ollama-intro-devcontainer/settings`
and set visibility to **Public** under "Danger Zone". May require org admin.

**Option B - grant repository access (private package).** On the same settings
page, add the repository with **Read** access under *both* "Manage Actions
access" and "Manage repository access". Both grants are needed for Codespaces
to authenticate the pull.

## Forks, and anyone who cannot pull the image

**A public GHCR package can be pulled by anyone, including forks** - GitHub's
docs state you "can also access public container images anonymously." So if the
package is Public (see the section above), forks work with no special handling.

The problem is only real when the package is **private**: a fork's Codespaces
token has no access to another org's private package, and creation fails.

### The fallback is a second dev container configuration, not a branch

This repo ships two configurations:

| Config | Path | What it does |
|---|---|---|
| **Ollama workshop (prebuilt image - fast)** | `.devcontainer/devcontainer.json` | Pulls the GHCR image. The default. |
| **Ollama workshop (build from source - forks / no GHCR)** | `.devcontainer/build-from-source/devcontainer.json` | Builds the same Dockerfile locally. 10-20 min the first time. |

Both are listed in the **Dev container configuration** dropdown on the
codespace creation options page, so a fork user picks the second one at
creation - nothing to edit, nothing to merge.

This is deliberately NOT a separate branch. A branch would mean every `labs.md`
and `README.md` change has to be applied twice, and the two copies drift.

Constraints worth knowing if you edit these:

- Alternative configs **must** live exactly one level below `.devcontainer/`.
  `.devcontainer/build-from-source/devcontainer.json` is valid;
  `.devcontainer/forks/testing/devcontainer.json` is not.
- In the fallback config, `dockerfile` and `context` are relative to *that*
  file, which is one level deeper - hence `"../Dockerfile"` and `"../.."`.
  The context must be the repo root because the Dockerfile does
  `COPY requirements.txt`.
- The `name` field is what shows in the dropdown. Keep both names descriptive.

### Prebuilds on a fork

To make the build-from-source path fast for a fork, set up a prebuild in the
fork: **Settings > Codespaces > Prebuilds > Set up prebuild**, for the `main`
branch, selecting the `build-from-source` configuration. The first prebuild
takes 10-20 minutes; creations after that use the cached result.

## Testing after a rebuild

Create a fresh codespace from `main` and confirm:

1. `ollama list` shows **llama3.2:3b** and NOT llama3.2:1b (the Lab 1 pull must still have work to do)
2. `py_env/` is populated and no `pip install` appeared in the creation log
3. `which ollama` returns `/usr/local/bin/ollama`
4. `claude --version` returns a version
5. `curl -sS http://localhost:11434/api/tags` answers - Ollama started on its own
6. The PORTS panel shows one entry, "Ollama API"
7. `code -d extra/Modelfile-shellcoach-complete.txt modelfiles/Modelfile.shellcoach`
   shows the yellow Merge Info bubbles in the left gutter
8. The **Dev container configuration** dropdown on the creation page offers both
   configs, and the build-from-source one still completes
9. `df -h` leaves comfortable free space
10. **Write test:** `ollama cp llama3.2:3b scratch && ollama rm scratch` - proves
   `/opt/ollama-models` is writable, which Labs 2 and 4 depend on
