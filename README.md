# Getting Started with Ollama

Repository for the *Getting Started with Ollama* hands-on workshop - running and using local LLMs.

**Revision 4.8 - 09/04/26**

<br/>

## Two ways to run the labs

Pick one. Everything in `labs.md` works either way.

| | | Best when |
| :-- | :-- | :-- |
| **Option A - GitHub Codespace** | Nothing to install. Ollama, Python, the packages and the default model are already in the image. | The default. Use this unless you cannot. |
| **Option B - Your own machine** | Install Ollama, Git and Python, and use your own editor. Windows, macOS or Linux. | No GitHub account, Codespaces blocked by policy, an offline room, or you just prefer local. |

**Both are covered below.** Option B is four installs and six commands. If you hit a snag - or want the
per-platform detail, the codespace commands that need a local equivalent, or troubleshooting -
**[local-setup.md](./local-setup.md)** has it. `labs.md` also carries **Running locally:** notes at each
step where the experience differs.

<br/>

## Before you start

**Everything in this workshop is free.** No paid API keys, no credit card. Labs 1 - 3 run entirely on local
models, wherever you run them.

**Lab 4 uses a large cloud-hosted model, which needs a free ollama.com account.** Creating one takes about a
minute. You do not need it to start - Lab 1 ends with a one-command `ollama signin` step, and Lab 4 will
prompt you if you skipped it. But if you would rather not spend workshop time on a signup form, create the
account ahead of time at https://ollama.com.

If your organization blocks account creation on external sites, that is fine - Lab 4 is the only lab that
needs it, and you can follow along without signing in.

<br/>

## Option A - Setup in a GitHub Codespace

**1. Change your codespace's default timeout from 30 minutes to 60 minutes.**

When logged in to GitHub, go to https://github.com/settings/codespaces and scroll down to the *Default idle timeout* section. Set it to 60 minutes so your codespace does not shut down mid-lab.

![Changing codespace idle timeout value](./images/ollama4.png?raw=true "Changing codespace idle timeout value")



<br><br>


**2. Click on the button below to start a new codespace from this repository.**

Click here ➡️  [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/skillrepos/ollama-intro?quickstart=1)

<br><br>

**3. Then click on the option to create a new codespace.**

![Creating new codespace from button](./images/ollama47.png?raw=true "Creating new codespace from button")

This runs for a couple of minutes while it pulls the prepared course image, which already contains the Python environment, Ollama, and the workshop's default model. You will pull a second model yourself in Lab 1.

The codespace is ready to use when you see output in the terminal similar to the following.

![Ready to use](./images/ollama53.png?raw=true "Ready to use")

**4. If VS Code shows a workspace trust prompt, click *Trust*.**

The codespace may open in Restricted Mode with a banner asking whether you trust the authors
of the files. Click **Trust** (or *Yes, I trust the authors*). 

![Trust workspace](./images/ollama48.png?raw=true "Trust workspace")

**5. Open up the *labs.md* file so you can follow along with the labs.**

You can either open it in a separate browser instance or open it in the codespace. If you open it in the codespace, make sure to *Open Preview* so you can see it in Markdown form as intended.

![Opening labs](./images/ollama3.png?raw=true "Opening labs")

<br/>

## Option B - Setup on your own machine

**Install four things, then run six commands.** That is the whole setup. Per-platform detail and
troubleshooting live in **[local-setup.md](./local-setup.md)** - you should not need it unless something
goes wrong.

| Install | Where |
| :-- | :-- |
| **Ollama 0.15 or later** - 0.15 is the minimum for Lab 4's `ollama launch` | https://ollama.com/download |
| **Git** - on Windows this also installs **Git Bash**, which you want | https://git-scm.com/downloads |
| **Python 3.10 or later** - tick *Add python.exe to PATH* on Windows | https://www.python.org/downloads/ |
| **Any editor you already like** - you need one that can show two files side by side for the two merge steps. VS Code is what the labs show; anything with a compare view works | https://code.visualstudio.com/download |

Then, in a terminal (**Git Bash** on Windows):

```
git clone https://github.com/skillrepos/ollama-intro.git
cd ollama-intro
python3 -m venv py_env
source py_env/bin/activate
pip install -r requirements.txt
ollama pull llama3.2:3b
```

*(Windows PowerShell users: `py_env\Scripts\activate` instead of the `source` line.)*

**That is the whole setup.** To confirm it worked, `ollama list` should show `llama3.2:3b` and
`curl http://localhost:11434` should answer `Ollama is running`. Then start at Lab 1.

Three things worth knowing before you begin:

- **On Windows, run the lab commands in Git Bash or WSL** - not PowerShell or cmd. The labs use `time`,
  pipes, and single-quoted JSON on `curl`, all of which behave differently there.
- **Lab 4 step 9 also wants Claude Code** - `npm install -g @anthropic-ai/claude-code`, which needs
  Node 18+. Every other step works without it.
- **Already running Docker Desktop?** Install the VS Code *Dev Containers* extension, open this repo and
  choose **Reopen in Container**. You get the codespace image with none of the above to install.

**Requirements:** about 6 GB of free disk and 8 GB of RAM. **No GPU needed** - the labs are written for
CPU-only machines, which is exactly what a codespace is. A GPU just makes everything faster.

<br/>

## License

For educational use only by the attendees of our workshops.

(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.
