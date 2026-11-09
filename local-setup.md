# Running the labs without a Codespace - per-platform detail

**Revision 1.6 - 11/09/26**

**Do the setup in [README.md](./README.md) - Option B first.** It is four installs and six commands, and
for most people that is the whole job.

This file is what sits behind those installs: the per-platform specifics, the steps in `labs.md` that
work differently on your machine (*Lab by lab*), and what to do when something breaks. Read the
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

`ollama --version` must report **0.15 or later** for Lab 4's `ollama launch` step; the codespace runs
0.40, and the screenshots in `labs.md` come from it. If the command is not found at all, close and reopen
the terminal so it picks up the new PATH.

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

- **`code <file>`** - steps that open a file to read or edit. Open it however you normally would.
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
your own machine, install it with Anthropic's installer:

- **macOS / Linux / WSL** - `curl -fsSL https://claude.ai/install.sh | bash`
- **Windows PowerShell** - `irm https://claude.ai/install.ps1 | iex`

(`npm install -g @anthropic-ai/claude-code` also works if you already have Node.js 18+.) Ollama may offer
to set it up for you when it is missing, but installing it first matches the codespace and takes the
uncertainty out of a live step.

Skip it and `ollama launch --help` in step 8 still works - you cannot complete step 9. **No Anthropic
account or API key is needed either way** - `ollama launch` points Claude Code at your local server. The
command needs **Ollama 0.15 or later**. The list of tools it can start grows with each release -
`ollama launch --help` shows the current one.

<br/>

## Lab by lab

`labs.md` is written for the codespace. Every `ollama` command, every `curl`, and every `python api/...`
program runs unchanged on your machine. These are the only steps that work differently; each one also has a
💻 **Running locally** box in `labs.md`.

**On Windows, run the lab commands in Git Bash or WSL, not PowerShell or cmd.** The `time` command, the
pipes, and the single-quoted JSON in the `curl` steps all behave differently in PowerShell.

| Where in `labs.md` | In the codespace | On your machine |
| :-- | :-- | :-- |
| Every lab - the repo folder | `cd /workspaces/ollama-intro` | `cd` to wherever you cloned the repo |
| Lab 1 step 2 | `llama3.2:3b` is already there | If `ollama list` is empty, run `ollama pull llama3.2:3b` first - step 3 fails without it |
| Lab 1 step 3, Lab 5 step 9 - start Ollama | `bash scripts/startOllama.sh` | **Windows/macOS:** launch the Ollama app from the tray or menu bar. **Linux:** `sudo systemctl start ollama`, or `ollama serve` in its own terminal |
| Lab 1 step 12 - `ollama signin` | the codespace terminal | any terminal |
| Lab 2 step 2 - `time` | works as shown | Use Git Bash or WSL on Windows. Your times will differ from the screenshot; compare the two models with each other |
| Lab 2 step 5, Lab 3 step 7 - `code -d` merges | VS Code's compare view | Any editor's compare view - see *An editor for the merge steps* above |
| Lab 4 step 9 - Claude Code | preinstalled | Install it first (see *Claude Code, for Lab 4 step 9* above), or accept `ollama launch`'s offer to set it up |
| Lab 5 - models staying loaded | pinned with `OLLAMA_KEEP_ALIVE=-1` | Models unload after 5 idle minutes, so the next prompt is slow. Run `python api/warmup.py` first, or pin them - see below |
| Lab 5 step 8 - server log | `tail -30 /tmp/ollama.log` | **macOS:** `cat ~/.ollama/logs/server.log` <br/>**Linux:** `journalctl -e -u ollama` <br/>**Windows:** `explorer %LOCALAPPDATA%\Ollama` - the newest file is `server.log` |
| Lab 5 step 9 - stop Ollama | `bash scripts/shutdown_ollama.sh` | **Windows:** quit Ollama from the system tray. **macOS:** quit it from the menu bar. **Linux:** `sudo systemctl stop ollama` |
| Speed | CPU only: 4 - 6 seconds for a short answer | Your hardware - a GPU is much faster |

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
| `address already in use` on 11434 | An Ollama server is already running. Stop it (see *Lab by lab*, Lab 5 step 9) before starting another |
| First prompt is slow, every time | The model unloaded after 5 minutes. Pin it with `OLLAMA_KEEP_ALIVE=-1` above, or re-run `python api/warmup.py` |
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
