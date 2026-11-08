## The labs

`labs.md` contains five labs. **The first four are what we work through together in the
two-hour session.** Lab 5 is written to the same standard and is yours to work through
afterward - it covers structured output and OpenAI compatibility (the two developer features
the clock does not allow us to type through) plus the troubleshooting commands you'll want
when working on your own.

Every lab is capped at **12 steps and 12 minutes**.

| Lab | Steps | Time | When |
| :-- | :-- | :-- | :-- |
| 1 - Running your first local model | 12 | 10 min | In class |
| 2 - Choosing a model and customizing it | 12 | 12 min | In class |
| 3 - Using Ollama from an application | 10 | 12 min | In class |
| 4 - Cloud models and wiring up your tools | 11 | 9 min | In class |
| 5 - Structured output, OpenAI compat, troubleshooting | 10 | 10 min | Take-home |

Lab 3 walks the four developer-facing ways into Ollama in order - the CLI (from Lab 1), raw
HTTP with `curl`, the official `ollama` Python library, and LangChain's `ChatOllama` - and
shows that all four hit the same endpoint with the same options and the same message shape.

**Lab 4 needs a free ollama.com account.** Lab 1 ends with an `ollama signin` step - run it
before you reach Lab 4 and Lab 4 starts on the interesting part.

<br/>

## Prerequisites

- A GitHub user ID on the public [GitHub.com](https://github.com) site (free tier is fine)
- Basic command-line familiarity
- Basic understanding of what an LLM is

No paid API keys are required. Everything in the in-class labs runs on free local models.

<br/>

## System requirements

The devcontainer requests 4 CPUs / 16 GB RAM / 32 GB storage. There is no GPU in a
codespace, so all inference is CPU-only. All figures below were measured on a real 4-core
codespace, not estimated:

| Operation | Typical time on a 4-core codespace |
| :-- | :-- |
| Codespace creation + setup scripts | 10 - 12 minutes |
| &nbsp;&nbsp;- of which: container build | 8 - 9 minutes |
| &nbsp;&nbsp;- of which: `startup_ollama.sh` (install + pull + warm) | under 1 minute |
| `ollama pull` (per model, ~2 GB) | 15 - 30 seconds |
| First prompt to a cold model | 5 - 10 seconds |
| Warm short prompt to `llama3.2:1b` | 2 - 3 seconds |
| Warm short prompt to `llama3.2:3b` | 4 - 6 seconds |
| Warm ~150-word answer from `llama3.2:3b` | 10 - 15 seconds |

Generation runs at roughly **55 ms/token on the 1B and 70 ms/token on the 3B**, so answer
length drives elapsed time far more than model choice does. If a prompt seems to hang,
it is almost always just slow CPU inference on a long answer. Give it a minute.

### Warmup

The labs default to `llama3.2:3b`. A **cold** model load costs about 5 seconds on top of
generation, so `api/warmup.py` pre-loads the workshop models and pins them in memory:

```
python api/warmup.py                 # warm the two workshop models
python api/warmup.py shellcoach      # warm a model you just created
python api/warmup.py llama3.2:3b 1h  # warm one model, hold it for an hour
```

Lab 1 runs this as step 3. `scripts/startOllama.sh` also runs it in the background every time
you reconnect to the codespace, and the server is started with `OLLAMA_KEEP_ALIVE=-1`, so once
loaded, models stay loaded for the life of the codespace - no re-warming between labs or after
a break. Under the hood the warmup is a POST to `/api/generate` with a model and no prompt -
students read the source in Lab 3.

<br/>

## Optional: using larger models

Labs 1 - 3 run entirely on free local models. **Lab 4** reaches a large hosted model on
Ollama Cloud's free tier, and take-home Lab 5 shows the API-key route:

1. **Ollama Cloud** - `ollama signin`, then pull a cloud-tagged model (for example
   `gpt-oss:120b-cloud`). It routes through your same local endpoint, so your code is unchanged.
   You can also go direct to `https://ollama.com` with an API key from
   https://ollama.com/settings/keys set as `OLLAMA_API_KEY`.
2. **OpenAI-compatible endpoint** - Ollama serves `/v1` so the official OpenAI SDK works
   against `http://localhost:11434/v1`. Swapping `base_url` to a hosted provider is a one-line change.
3. **`ollama launch`** - configures and starts a real coding tool (Claude Code, OpenCode,
   Codex, VS Code, Droid) against a local or cloud model, with no config files to edit.
   Requires Ollama 0.15 or later.

The free tier covers light usage with one cloud model at a time. It is enough for Lab 4.

Cloud model names change frequently. Check the current list at https://ollama.com/search?c=cloud
before relying on one.

<br/>

## Alternative setup (local machine instead of a codespace)

See **[local-setup.md](./local-setup.md)** for the full walkthrough - installing Ollama on
Windows, macOS, and Linux, cloning the repo, setting up Python, and the handful of codespace
commands in `labs.md` that need a local equivalent.

The short version: install Docker Desktop and the VS Code *Dev Containers* extension, clone
the repo, open it in VS Code, and choose *Reopen in Container*. That gives you the same image
the codespace uses and every lab command works unchanged. `local-setup.md` also covers the
native route if you would rather not use Docker.

<br/>

## Security: before you expose Ollama to anything

Ollama's API has no authentication. There is no token, no user, no access control - anyone who
can reach port 11434 can list your models, run inference on your hardware, pull or delete
models, and (given the right bug) read the server process's memory. The only control that
matters is what the server binds to.

**In the workshop this is already handled.** The devcontainer sets `OLLAMA_HOST=127.0.0.1:11434`,
so the server listens on loopback only and nothing outside the codespace can reach it.

**On your own machine** the same loopback default applies until you change it. The common
mistake is setting `OLLAMA_HOST=0.0.0.0:11434` so another machine can reach Ollama - that
publishes an unauthenticated API to the whole network you are on. If you need remote access,
put a reverse proxy that requires authentication in front of it, or reach it over a private
network or tunnel. Do not open the port directly.

Three more habits worth having:

- Keep Ollama current. Every issue below was fixed in a release.
- Only build models from GGUF files you trust - `ollama create` parses the file, and a hostile one has been enough.
- Assume anything in the server's environment is reachable by a successful attacker. Do not leave unrelated API keys there.

### Known vulnerabilities

| CVE | What it is | Fixed in |
| :-- | :-- | :-- |
| [CVE-2024-37032](https://www.wiz.io/blog/probllama-ollama-vulnerability-cve-2024-37032) ("Probllama") | Path traversal in the model-pull path leading to remote code execution | 0.1.34 |
| [CVE-2025-63389](https://github.com/advisories/GHSA-f6mr-38g8-39rg) | Model-management endpoints reachable with no authentication | see note below |
| [CVE-2026-7482](https://www.cyera.com/research/bleeding-llama-critical-unauthenticated-memory-leak-in-ollama) ("Bleeding Llama", CVSS 9.1) | Heap out-of-bounds read in the GGUF model loader, triggered through `/api/create` with a crafted model file. Leaked environment variables, API keys, system prompts, and other users' in-flight conversations | 0.17.1 |

CVE-2025-63389 is Ollama's documented design recorded as a CVE rather than a bypass of anything -
there was never authentication to bypass. The published version ranges do not agree: OSV lists it
as fixed after v0.12.3, while the GitHub advisory lists everything through 0.13.5 as affected with
no patched version given. Either way the mitigation is the binding, not a version bump.

The workshop codespace runs Ollama 0.32.9, which is past all three fixes.

<br/>

## Troubleshooting

| Symptom | Fix |
| :-- | :-- |
| `Error: could not connect to ollama app` | `bash scripts/startOllama.sh` |
| `address already in use` on 11434 | `bash scripts/shutdown_ollama.sh` then start it again |
| `model 'x' not found` | `ollama pull x` - check spelling with `ollama list` |
| Prompt appears frozen | CPU inference is slow on long answers. Wait 60 seconds before assuming failure. |
| `ERROR: This version requires zstd for extraction` | The base image ships without `zstd`. The setup scripts now install it automatically; if you hit this on an older codespace, run `sudo apt-get install -y zstd` then `curl -fsSL https://ollama.com/install.sh \| sh`. |
| VS Code shows a "Restricted Mode" / workspace trust banner | Click **Trust** (or "Yes, I trust the authors"). Until you do, the `code -d` merge steps in Labs 2 and 3 will not open. |
| First prompt very slow | The model unloaded (should not happen in the codespace - `OLLAMA_KEEP_ALIVE=-1` pins them). Run `python api/warmup.py` |
| `ollama launch` not found | Needs Ollama 0.15+. Check `ollama --version` |
| Codespace out of disk | `ollama rm <model>` for models you are done with |
| Want to see the server log | `tail -f /tmp/ollama.log` |

<br/>

## Repository layout

```
ollama-intro/
├── .devcontainer/         devcontainer.json for Codespaces / Dev Containers
├── .github/               copilot-instructions.md
├── api/                   Python programs: warmup, REST, library, LangChain
├── extra/                 Completed versions of the skeleton files (for diff-merge)
├── images/                Screenshots referenced in labs.md
├── modelfiles/            Modelfile used in Lab 2
├── scripts/               Environment and Ollama setup scripts
├── extra.md               This file - lab overview, timings, security notes, troubleshooting
├── IMAGEMAINTENANCE.md    When and how to rebuild the prebuilt container image
├── labs.md                THE lab document - Labs 1-4 in class, Lab 5 take-home
├── local-setup.md         Running the labs without a codespace (Windows/macOS/Linux)
├── merge-info.json        Hover notes for the diff-merge steps
├── README.md              Codespace setup
└── requirements.txt
```

<br/>
