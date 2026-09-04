# Running the labs without a Codespace

**Revision 1.2 - 09/04/26**

The workshop is built around GitHub Codespaces, and `README.md` covers that path. Use
this file instead if you cannot use a codespace - no GitHub account, a blocked network,
an org policy against Codespaces, or you simply prefer your own machine.

Everything in `labs.md` works locally. What changes is that a few commands written for
the codespace need a local equivalent, and you have to install things the course image
provides for you. Both are covered below.

`labs.md` also carries a **Running these labs on your own machine** section near the top and
a **Running locally:** note at each individual step where your experience differs - so you can
work straight through it once the setup here is done.

<br/>

## The short version

Install **Ollama 0.15+**, **Git**, **Python 3.10+**, and use whatever **editor** you already have. Then:

```
git clone https://github.com/skillrepos/ollama-intro.git
cd ollama-intro
python3 -m venv py_env
source py_env/bin/activate
pip install -r requirements.txt
ollama pull llama3.2:3b
```

*(Windows PowerShell: `py_env\Scripts\activate` instead of the `source` line. But use Git Bash for the
labs themselves - see below.)*

Check it: `ollama list` shows `llama3.2:3b`, and `curl http://localhost:11434` answers `Ollama is running`.
If both pass, **skip to [Codespace commands and their local equivalents](#codespace-commands-and-their-local-equivalents)**
- that short table is the only part of this file you actually need while running the labs.

The numbered sections below are reference: read the one that matches whatever gave you trouble.

<br/>

## Two ways to run locally

| | What you need | Best when |
| :-- | :-- | :-- |
| **A. Dev Container** | Docker Desktop + VS Code + *Dev Containers* extension | You want the exact codespace environment with nothing to configure |
| **B. Native install** | Ollama, Git, Python, an editor | You do not want Docker, or Docker is blocked too |

**Option A is far less work.** Install Docker Desktop and the VS Code *Dev Containers*
extension, clone the repo (step 2 below), open the folder in VS Code, and choose
**Reopen in Container** when prompted. You get the same image the codespace uses -
Ollama, Python, both scripts, and the default model already in place - and every command
in `labs.md` works exactly as written. Skip the rest of this file.

The remainder covers **Option B**.

<br/>

## Before you start

You need roughly **6 GB of free disk** for Ollama plus the two workshop models, and at
least **8 GB of RAM**. A GPU is not required - the workshop is written for CPU-only
machines, which is what a codespace is.

**On Windows, run the lab commands in Git Bash or WSL, not PowerShell or cmd.** The labs
use `time`, pipes, and single-quoted JSON on `curl` - all of which behave differently in
PowerShell. Git Bash ships with Git for Windows (step 2) and makes every command in
`labs.md` work exactly as printed.

<br/>

## 1. Install Ollama

### Windows

Download and run the installer from **https://ollama.com/download/windows**. It installs
to `%LOCALAPPDATA%\Programs\Ollama` and starts Ollama in the system tray, which also
starts the local server.

### macOS

Download the app from **https://ollama.com/download/mac**, unzip it, and drag
**Ollama.app** to *Applications*. Launch it once - it puts an icon in the menu bar and
starts the local server. Homebrew (`brew install ollama`) also works but can lag the
official release.

### Linux

```
curl -fsSL https://ollama.com/install.sh | sh
```

The script installs the binary and, on systemd distributions, sets up and starts an
`ollama` service. If your distribution does not use systemd, start the server yourself
with `ollama serve` and leave it running in its own terminal.

### Verify

Open a terminal (**Git Bash** on Windows) and run:

```
ollama --version
```

You need **0.15 or later** for Lab 4's `ollama launch` step. If the command is not found,
close and reopen the terminal so it picks up the new PATH.

<br/>

## 2. Install Git and clone the repository

### Windows

Install **Git for Windows** from https://git-scm.com/download/win. Accept the defaults -
this also gives you the **Git Bash** terminal you will use for the labs. Then open Git
Bash and run the clone command below.

### macOS

Git is included with the Xcode command line tools. If `git --version` prompts you to
install them, accept. Otherwise `brew install git`.

### Linux

```
sudo apt-get install -y git        # Debian / Ubuntu
sudo dnf install -y git            # Fedora / RHEL
```

### Clone (all three platforms)

```
git clone https://github.com/skillrepos/ollama-intro.git
```
```
cd ollama-intro
```

**Wherever `labs.md` says `cd /workspaces/ollama-intro`, it means this folder.** That path
only exists inside a codespace.

<br/>

## 3. Set up Python

You need **Python 3.10 or later**. Check with `python3 --version` (Windows: `python --version`).
If it is missing, install it from https://www.python.org/downloads/ - on Windows, tick
**"Add python.exe to PATH"** in the installer.

Create a virtual environment in the repo folder and install the four packages the lab
programs use:

**macOS / Linux / Git Bash on Windows**

```
python3 -m venv py_env
```
```
source py_env/bin/activate
```
```
pip install -r requirements.txt
```

**Windows PowerShell** (if you are not using Git Bash for this part)

```
python -m venv py_env
```
```
py_env\Scripts\activate
```
```
pip install -r requirements.txt
```

Activate the environment in every new terminal before running the `python api/...`
commands in the labs. You will know it is active because your prompt starts with
`(py_env)`, the same as it does in the codespace.

<br/>

## 4. Pull the default model

**Do not skip this.** The codespace image ships with `llama3.2:3b` already downloaded, so
`labs.md` never tells you to pull it - Lab 1 step 2 only pulls the 1B. On your own machine
you have neither, and Lab 1 step 3 will fail without the 3B.

```
ollama pull llama3.2:3b
```

That is about 2 GB. Lab 1 step 2 pulls `llama3.2:1b` (about 1.3 GB) as part of the lab -
let it do that rather than pulling it now, or the step becomes a no-op.

Confirm:

```
ollama list
```

<br/>

## 5. An editor for the merge steps

**You do not need VS Code.** Any editor works. The labs ask an editor to do two things:

- **`code <file>`** - steps that just open a file to read or edit. Open it however you normally would.
- **`code -d <complete> <skeleton>`** - Labs 2 and 3 show a side-by-side diff and have you merge the left
  side into the right. Any compare view does this: VS Code, IntelliJ / PyCharm, Sublime Merge, BBEdit,
  Meld, `vimdiff`, `kdiff3`.

If your editor has no compare view, open both files and copy the blocks that are in the complete file but
not in the skeleton. That is the same exercise - the point is reading each block before you take it, not
the tool. There are only two pairs in the whole workshop:

| Lab | Complete file | Skeleton you edit |
| :-- | :-- | :-- |
| 2 step 5 | `extra/Modelfile-shellcoach-complete.txt` | `modelfiles/Modelfile.shellcoach` |
| 3 step 7 | `extra/chat_app-complete.txt` | `api/chat_app.py` |

A terminal `diff` shows you exactly what to move:

```
diff -u modelfiles/Modelfile.shellcoach extra/Modelfile-shellcoach-complete.txt
```

**If you do use VS Code**, install it from https://code.visualstudio.com/download and make sure the `code`
command is on your PATH, so the lab commands work exactly as printed:

- **Windows** - the installer adds `code` to PATH automatically.
- **Linux** - the `.deb` / `.rpm` packages add it automatically.
- **macOS** - open VS Code, press `CMD+SHIFT+P`, and run
  **Shell Command: Install 'code' command in PATH**.

Optionally install the **Merge Info** extension bundled at `.devcontainer/merge-info-0.1.0.vsix` for hover
explanations on each merge block. It is a VS Code-only nicety - the merges work fine without it.

```
code --install-extension .devcontainer/merge-info-0.1.0.vsix
```

<br/>

## 6. Optional - Claude Code, for Lab 4 step 9

Lab 4 step 9 runs `ollama launch claude`, which starts Claude Code against an Ollama
model. The codespace image preinstalls it. On your own machine, install it yourself with
Node.js 18+:

```
npm install -g @anthropic-ai/claude-code
```

Recent Ollama versions may offer to set the tool up for you when it is missing, but having it
already installed matches what the codespace does and takes the uncertainty out of a live step.

Skip this and `ollama launch --help` in step 8 still works - you just cannot complete
step 9. **No Anthropic account or API key is needed either way** - `ollama launch` points Claude
Code at your local server. `ollama launch` needs **Ollama 0.15 or later** and currently drives
Claude Code, OpenCode, Codex, VS Code and Droid.

<br/>

## Codespace commands and their local equivalents

`labs.md` is written for the codespace. These are the only places that matters.

| `labs.md` says | On your machine |
| :-- | :-- |
| `cd /workspaces/ollama-intro` | `cd` to wherever you cloned the repo |
| `bash scripts/startOllama.sh` <br/>(Lab 1 step 3, Lab 5 step 9) | **Windows/macOS:** the Ollama app starts the server - launch it from the tray or menu bar. <br/>**Linux:** `sudo systemctl start ollama`, or `ollama serve` in its own terminal |
| `bash scripts/shutdown_ollama.sh` <br/>(Lab 5 step 9) | **Windows:** quit Ollama from the system tray. <br/>**macOS:** quit it from the menu bar. <br/>**Linux:** `sudo systemctl stop ollama` |
| `tail -30 /tmp/ollama.log` <br/>(Lab 5 step 8) | **macOS:** `cat ~/.ollama/logs/server.log` <br/>**Linux:** `journalctl -e -u ollama` <br/>**Windows:** `explorer %LOCALAPPDATA%\Ollama` - most recent is `server.log` |
| "This codespace pins models in memory" <br/>(Lab 5 intro) | Locally the default is **5 minutes**, then the model unloads and the next prompt pays a reload. Run `python api/warmup.py` again, or see below to pin them |

To pin models the way the codespace does, set `OLLAMA_KEEP_ALIVE=-1` in the environment
the *server* runs in - not the terminal you type in:

- **Windows** - System Properties > Environment Variables, add `OLLAMA_KEEP_ALIVE` = `-1`, then quit and relaunch Ollama from the tray
- **macOS** - `launchctl setenv OLLAMA_KEEP_ALIVE -1`, then quit and relaunch the app
- **Linux** - `sudo systemctl edit ollama`, add `Environment="OLLAMA_KEEP_ALIVE=-1"` under `[Service]`, then `sudo systemctl restart ollama`

Everything else in `labs.md` - every `ollama` command, every `curl`, every `python api/...`
program - runs unchanged.

<br/>

## Check your setup before Lab 1

Run these four from the repo folder with `py_env` active. All four should succeed.

```
ollama --version
```
```
ollama list
```
```
curl http://localhost:11434
```
```
python api/warmup.py
```

You want: version 0.15+, `llama3.2:3b` in the list, `Ollama is running` from the curl, and
warmup reporting the model loaded. If all four pass, start at Lab 1 step 1.

<br/>

## Troubleshooting

| Symptom | Fix |
| :-- | :-- |
| `ollama: command not found` | Close and reopen the terminal so it picks up the new PATH. On Linux, confirm with `which ollama` |
| `curl: (7) Failed to connect to localhost port 11434` | The server is not running. Windows/macOS: launch the Ollama app. Linux: `sudo systemctl start ollama` or `ollama serve` |
| `Error: model 'llama3.2:3b' not found` | You skipped step 4 above. Run `ollama pull llama3.2:3b` |
| `code -d` opens nothing | Using VS Code? The `code` command is not on PATH - see step 5. Not using VS Code? Use your editor's compare view, or `diff -u` - step 5 lists the two file pairs |
| `ModuleNotFoundError: No module named 'ollama'` | The virtual environment is not active. Re-run the activate command for your platform |
| `time: command not found` (Lab 2 step 2) | You are in PowerShell or cmd. Use Git Bash or WSL |
| Multi-line `curl` in Lab 3 errors out | Same cause - PowerShell parses the single-quoted JSON differently. Use Git Bash or WSL |
| `address already in use` on 11434 | An Ollama server is already running. Stop it (see the equivalents table) before starting another |
| First prompt is very slow, every time | The model unloaded after 5 minutes. Pin it with `OLLAMA_KEEP_ALIVE=-1` above, or re-run `python api/warmup.py` |
| Answers are much slower than the times in `extra.md` | Those figures are from a 4-core CPU-only codespace. Your machine may be faster or slower; long answers scale with length either way |

<br/>

## What you will not have

Two conveniences are codespace-only and are not worth reproducing:

- **The prebuilt image.** Your first run downloads Ollama, the Python packages, and the
  models rather than getting them preinstalled.
- **Auto-start on reconnect.** `scripts/postattach.sh` restarts Ollama and warms the
  models each time you reconnect to a codespace. Locally, the Ollama app handles starting
  the server, and `python api/warmup.py` handles the warming when you want it.

Neither affects a single lab step.
