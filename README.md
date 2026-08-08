# Getting Started with Ollama

Repository for the *Getting Started with Ollama* hands-on workshop - running and using local LLMs.

**Revision 3.3 - 08/07/26**

These instructions will guide you through configuring a GitHub Codespaces environment that you can use to run the course labs.

<br/>

## Setup

**1. Click on the button below to start a new codespace from this repository.**

Click here ➡️  [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/skillrepos/ollama-intro?quickstart=1)

**2. Then click on the option to create a new codespace.**

![Creating new codespace from button](./images/ollama1.png?raw=true "Creating new codespace from button")

This will run for several minutes while it gets everything ready.

After the initial startup, it runs two scripts:
- `scripts/pysetup.sh` creates the Python virtual environment and installs the requirements
- `scripts/startup_ollama.sh` installs Ollama, starts the service, and pre-pulls **llama3.2:3b** (the workshop default) and **llama3.2:1b**

Pre-pulling the models up front is deliberate - it means the first lab prompt in class is fast instead of waiting on a 2 GB download.

The codespace is ready to use when you see the `Ready for lab exercises!` banner in the terminal.

![Ready to use](./images/ollama2.png?raw=true "Ready to use")

**3. If VS Code shows a workspace trust prompt, click *Trust*.**

The codespace may open in Restricted Mode with a banner asking whether you trust the authors
of the files. Click **Trust** (or *Yes, I trust the authors*). Until you do, the `code -d`
diff-and-merge steps in Labs 2 and 3 will not open.

**4. Open up the *labs.md* file so you can follow along with the labs.**

You can either open it in a separate browser instance or open it in the codespace. If you open it in the codespace, make sure to *Open Preview* so you can see it in Markdown form as intended.

![Opening labs](./images/ollama3.png?raw=true "Opening labs")

**5. Change your codespace's default timeout from 30 minutes to 60 minutes.**

When logged in to GitHub, go to https://github.com/settings/codespaces and scroll down to the *Default idle timeout* section. Set it to 60 minutes so your codespace does not shut down mid-lab.

![Changing codespace idle timeout value](./images/ollama4.png?raw=true "Changing codespace idle timeout value")

**Now, you are ready for the labs!**

<br/>

## The labs

`labs.md` contains seven labs. **The first four are what we work through together in the
two-hour session.** Labs 5 - 7 are written to the same standard and are yours to work through
afterward - they go deeper on material the slides cover but the clock does not allow us to
type through.

Every lab is capped at **12 steps and 12 minutes**.

| Lab | Steps | Time | When |
| :-- | :-- | :-- | :-- |
| 1 - Running your first local model | 12 | 10 min | In class |
| 2 - Choosing a model and customizing it | 12 | 12 min | In class |
| 3 - Using Ollama from an application | 11 | 12 min | In class |
| 4 - Cloud models and wiring up your tools | 11 | 9 min | In class |
| 5 - Managing models on disk and in memory | 10 | 10 min | Take-home |
| 6 - The REST API in depth | 8 | 10 min | Take-home |
| 7 - Troubleshooting toolkit | 11 | 8 min | Take-home |

Lab 3 walks the four developer-facing ways into Ollama in order - the CLI (from Lab 1), raw
HTTP with `curl`, the official `ollama` Python library, and LangChain's `ChatOllama` - and
shows that all four hit the same endpoint with the same options and the same message shape.

**Lab 4 needs a free ollama.com account.** Lab 1 ends with an optional `ollama signin` step -
run it during the break and Lab 4 starts on the interesting part.

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

Lab 1 runs this as step 2. `scripts/startOllama.sh` also runs it in the background every time
you reconnect to the codespace, so your models are ready when you are. Under the hood it is a
POST to `/api/generate` with a model and no prompt - students read the source in Lab 3.

<br/>

## Optional: using larger models

Labs 1 - 3 run entirely on free local models. **Lab 4** reaches a large hosted model on
Ollama Cloud's free tier, and take-home Lab 7 shows the API-key route:

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

If you prefer to run locally, you need Docker Desktop and VS Code with the *Dev Containers*
extension. Clone the repo, open it in VS Code, and choose *Reopen in Container*. Everything
else in `labs.md` works the same.

To run without a container at all: install Ollama from https://ollama.com/download,
run `pip install -r requirements.txt`, and start at Lab 1.

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
| First prompt very slow | The model unloaded. Run `python api/warmup.py` |
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
├── anticipated-qa.md      Instructor prep: likely student questions
├── labs.md                THE lab document - Labs 1-4 in class, 5-7 take-home
├── README.md
└── requirements.txt
```

<br/>

## License

For educational use only by the attendees of our workshops.

(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.
