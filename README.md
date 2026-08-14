# Getting Started with Ollama

Repository for the *Getting Started with Ollama* hands-on workshop - running and using local LLMs.

**Revision 4.4 - 08/13/26**

These instructions will guide you through configuring a GitHub Codespaces environment that you can use to run the course labs.

<br/>

## Before you start

**Everything in this workshop is free.** No paid API keys, no credit card. Labs 1 - 3 run entirely on local
models in your codespace.

**Lab 4 uses a large cloud-hosted model, which needs a free ollama.com account.** Creating one takes about a
minute. You do not need it to start - Lab 1 ends with a one-command `ollama signin` step, and Lab 4 will
prompt you if you skipped it. But if you would rather not spend workshop time on a signup form, create the
account ahead of time at https://ollama.com.

If your organization blocks account creation on external sites, that is fine - Lab 4 is the only lab that
needs it, and you can follow along without signing in.

<br/>

## Setup

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


## License

For educational use only by the attendees of our workshops.

(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.
