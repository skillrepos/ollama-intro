# Running the labs without a Codespace - per-platform detail

**Revision 1.3 - 09/04/26**

**Do the setup in [README.md](./README.md) - Option B first.** It is four installs and six commands, and
for most people that is the whole job.

This file is what sits behind those installs: the per-platform specifics, the handful of codespace
commands in `labs.md` that need a local equivalent, and what to do when something breaks. Read the
section that matches your problem - it is not meant to be read front to back.

<br/>

## A shortcut, if you already run Docker

Install Docker Desktop and the VS Code *Dev Containers* extension, clone the repo, open the folder in
VS Code and choose **Reopen in Container**. You get the exact image the codespace uses - Ollama, Python,
the scripts, and the default model already in place - and every command in `labs.md` works as written,
including the `scripts/*.sh` ones. Nothing else in this file applies.

Everything below assumes a native install instead.

<br/>

## Per-platform install notes

### Ollama

- **Windows** - installer at https://ollama.com/download/windows. It installs to
  `%LOCALAPPDATA%\Programs\Ollama` and puts Ollama in the system tray, which is what starts the local
  server.
- **macOS** - app at https://ollama.com/download/mac. Unzip, drag **Ollama.app** to *Applications*, and
  launch it once - it puts an icon in the menu bar and starts the server. `brew install ollama` also
  works but can lag the official release.
- **Linux** - `curl -fsSL https://ollama.com/install.sh | sh`. On systemd distributions this also sets up
  and starts an `ollama` service. If yours is not systemd, run `ollama serve` in its own terminal and
  leave it there.

`ollama --version` must report **0.15 or later** for Lab 4's `ollama launch` step. If the command is not
found at all, close and reopen the terminal so it picks up the new PATH.

### Git

- **Windows** - **Git for Windows** from https://git-scm.com/download/win, defaults are fine. This is also
  where **Git Bash** comes from, and you want it: the labs use `time`, pipes and single-quoted JSON on
  `curl`, none of which behave the same in PowerShell or cmd. Run the labs in Git Bash or WSL.
- **macOS** - included with the Xcode command line tools. If `git --version` offers to install them,
  accept. Otherwise `brew install git`.
- **Linux** - `sudo apt-get install -y git` (Debian/Ubuntu) or `sudo dnf install -y git` (Fedora/RHEL).

### Python

**3.10 or later.** Check with `python3 --version`, or `python --version` on Windows. Installer at
https://www.python.org/downloads/ - on Windows, tick **"Add python.exe to PATH"**.

Two things about the virtual environment:

- **Activate it in every new terminal** before any `python api/...` command. Your prompt starts with
  `(py_env)` when it is active, the same as it does in the codespace.
- **Windows PowerShell** activates with `py_env\Scripts\activate` rather than the `source` line in the
  README. In Git Bash, use the `source` line as printed.

### The models

`ollama pull llama3.2:3b` is in the README setup because the codespace image ships with it and `labs.md`
therefore never tells you to pull it. Lab 1 step 3 fails without it.

**Do not also pre-pull `llama3.2:1b`.** Lab 1 step 2 pulls it, and that step is the point - pull it now
and the step becomes a no-op.

<br/>

## An editor for the merge steps

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

**If you do use VS Code**, make sure the `code` command is on your PATH so the lab commands work exactly
as printed. The Windows installer and the Linux `.deb`/`.rpm` packages do this for you; on macOS, open
VS Code, press `CMD+SHIFT+P` and run **Shell Command: Install 'code' command in PATH**.

Optionally install the **Merge Info** extension bundled at `.devcontainer/merge-info-0.1.0.vsix` for hover
explanations on each merge block. It is a VS Code-only nicety - the merges work fine without it.

```
code --install-extension .devcontainer/merge-info-0.1.0.vsix
```

<br/>

## Claude Code, for Lab 4 step 9

`ollama launch claude` starts Claude Code against an Ollama model. The codespace image preinstalls it; on
your own machine, `npm install -g @anthropic-ai/claude-code` (needs Node.js 18+). Recent Ollama versions
may offer to set it up for you when it is missing, but installing it first matches the codespace and takes
the uncertainty out of a live step.

Skip it and `ollama launch --help` in step 8 still works - you just cannot complete step 9. **No Anthropic
account or API key is needed either way** - `ollama launch` points Claude Code at your local server. The
command needs **Ollama 0.15 or later** and currently drives Claude Code, OpenCode, Codex, VS Code and Droid.

<br/>

## Codespace commands and their local equivalents

`labs.md` is written for the codespace. These are the only places that matters - it also flags each one
inline, as a **Running locally:** note at the step itself.

| `labs.md` says | On your machine |
| :-- | :-- |
| `cd /workspaces/ollama-intro` | `cd` to wherever you cloned the repo |
| `bash scripts/startOllama.sh` <br/>(Lab 1 step 3, Lab 5 step 9) | **Windows/macOS:** the Ollama app starts the server - launch it from the tray or menu bar. <br/>**Linux:** `sudo systemctl start ollama`, or `ollama serve` in its own terminal |
| `bash scripts/shutdown_ollama.sh` <br/>(Lab 5 step 9) | **Windows:** quit Ollama from the system tray. <br/>**macOS:** quit it from the menu bar. <br/>**Linux:** `sudo systemctl stop ollama` |
| `tail -30 /tmp/ollama.log` <br/>(Lab 5 step 8) | **macOS:** `cat ~/.ollama/logs/server.log` <br/>**Linux:** `journalctl -e -u ollama` <br/>**Windows:** `explorer %LOCALAPPDATA%\Ollama` - most recent is `server.log` |
| "This codespace pins models in memory" <br/>(Lab 5 intro) | Locally the default is **5 minutes**, then the model unloads and the next prompt pays a reload. Run `python api/warmup.py` again, or pin them - see below |

Everything else in `labs.md` - every `ollama` command, every `curl`, every `python api/...` program - runs
unchanged.

### Pinning models in memory

To hold models the way the codespace does, set `OLLAMA_KEEP_ALIVE=-1` in the environment the **server**
runs in - not the terminal you type in:

- **Windows** - System Properties > Environment Variables, add `OLLAMA_KEEP_ALIVE` = `-1`, then quit and
  relaunch Ollama from the tray
- **macOS** - `launchctl setenv OLLAMA_KEEP_ALIVE -1`, then quit and relaunch the app
- **Linux** - `sudo systemctl edit ollama`, add `Environment="OLLAMA_KEEP_ALIVE=-1"` under `[Service]`,
  then `sudo systemctl restart ollama`

<br/>

## Troubleshooting

| Symptom | Fix |
| :-- | :-- |
| `ollama: command not found` | Close and reopen the terminal so it picks up the new PATH. On Linux, confirm with `which ollama` |
| `curl: (7) Failed to connect to localhost port 11434` | The server is not running. Windows/macOS: launch the Ollama app. Linux: `sudo systemctl start ollama` or `ollama serve` |
| `Error: model 'llama3.2:3b' not found` | You skipped the `ollama pull llama3.2:3b` line in the README setup. Run it now |
| `code -d` opens nothing | Using VS Code? The `code` command is not on PATH. Not using VS Code? Use your editor's compare view, or `diff -u` - see *An editor for the merge steps* above |
| `ModuleNotFoundError: No module named 'ollama'` | The virtual environment is not active. Re-run the activate command for your platform |
| `time: command not found` (Lab 2 step 2) | You are in PowerShell or cmd. Use Git Bash or WSL |
| Multi-line `curl` in Lab 3 errors out | Same cause - PowerShell parses the single-quoted JSON differently. Use Git Bash or WSL |
| `address already in use` on 11434 | An Ollama server is already running. Stop it (see the equivalents table) before starting another |
| First prompt is very slow, every time | The model unloaded after 5 minutes. Pin it with `OLLAMA_KEEP_ALIVE=-1` above, or re-run `python api/warmup.py` |
| Answers are much slower than the quoted times | Those figures come from a 4-core CPU-only codespace. Your machine may be faster or slower; long answers scale with length either way |

<br/>

## What you will not have

Two conveniences are codespace-only and are not worth reproducing:

- **The prebuilt image.** Your first run downloads Ollama, the Python packages, and the model rather than
  getting them preinstalled.
- **Auto-start on reconnect.** `scripts/postattach.sh` restarts Ollama and warms the models each time you
  reconnect to a codespace. Locally, the Ollama app handles starting the server, and
  `python api/warmup.py` handles the warming when you want it.

Neither affects a single lab step.
