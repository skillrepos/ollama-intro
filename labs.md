# Getting Started with Ollama
## Running and using local LLMs 
## Session labs
## Revision 6.19 - 11/09/26

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

**NOTE: To copy and paste in the codespace, you may need to use keyboard commands - CTRL-C and CTRL-V. Chrome may work best for this.**

**NOTE: Run every command from the root of the repository unless a step says otherwise. You can always get back there with `cd /workspaces/ollama-intro`.**

**NOTE: This is a CPU-only codespace. A short answer from `llama3.2:3b` takes about 4 - 6 seconds; long answers take longer. That is normal.**

**Running on your own machine instead?** Do the setup in [README.md](./README.md) - Option B, and keep [local-setup.md](./local-setup.md) open. Its *Lab by lab* section lists every step that works differently outside the codespace.

**Labs 1 - 4 are in-class.** Lab 5 is optional if we have time, or you can do it later. Steps marked **(Optional)** are for people who finish early.

**Lab 4 needs an ollama.com account.** Creating one is free and takes about a minute; Lab 1 step 12 does it. Lab 4's cloud steps may cost a few cents, because Ollama's cloud charges per token. If a step says you need credits, follow along on the instructor's screen.

<br><br>

<p align="center">
<b>PART ONE - IN-CLASS LABS</b>
</p>

<br>

**Lab 1 - Running your first local model**

**Purpose: Warm up the models, run one locally, and learn the session commands.**

1. In the *TERMINAL* tab at the bottom of the codespace, check which version of Ollama is installed.

```
ollama --version
```

![Checking the Ollama version](./images/ollama5.png?raw=true "Checking the Ollama version")

<br><br>

2. List the models on disk, add the smaller 1B model, then list again. Both should show.

```
ollama list
```
```
ollama pull llama3.2:1b
```
```
ollama list
```

![Listing installed models](./images/ollama7.png?raw=true "Listing installed models")

<br><br>

3. Load both models into memory now, so later steps don't have to wait for it.

```
python api/warmup.py
```

![Warming up the models](./images/ollama6.png?raw=true "Warming up the models")

   If it says it could not reach Ollama, run `bash scripts/startOllama.sh` and try again.

<br><br>

4. Start a chat session with the 3B model.

```
ollama run llama3.2:3b
```

<br><br>

5. At the `>>>` prompt, ask a question, then a follow-up that only makes sense after the first answer.

```
In two sentences, what is the difference between a model and a checkpoint?
```
```
Why does that matter to a developer? Two sentences.
```

![First prompts to a local model](./images/ollama8.png?raw=true "First prompts to a local model")

<br><br>

6. List the session's commands, then show the model's details.

```
/?
```
```
/show info
```

![Model info from inside a session](./images/ollama9.png?raw=true "Model info from inside a session")

<br><br>

7. `num_predict` caps how long an answer can be. Set it low and ask for a long answer.

```
/set parameter num_predict 20
```
```
Explain what a container image is.
```

   The answer stops mid-sentence. Raise the cap, clear the conversation (the setting stays), and ask again.

```
/set parameter num_predict 200
```
```
/clear
```
```
Explain what a container image is.
```

![Capping the answer length with num_predict](./images/ollama10.png?raw=true "Capping the answer length with num_predict")

<br><br>

8. Leave the session. Use `/bye` - typing "exit" sends the word to the model as a question.

```
/bye
```

<br><br>

9. See which models are still in memory, and until when.

```
ollama ps
```

![Models currently loaded in memory](./images/ollama11.png?raw=true "Models currently loaded in memory")

<br><br>

10. Run one prompt straight from the command line - the way you would in a script.

```
ollama run llama3.2:3b "List three reasons to run an LLM locally. One short line each."
```

![One-shot prompt from the command line](./images/ollama12.png?raw=true "One-shot prompt from the command line")

<br><br>

11. (Optional) Send a file into it, like any other command.

```
cat requirements.txt | ollama run llama3.2:3b "What is this dependency file for? Two sentences."
```

<br><br>

12. Sign in now so you're ready for Lab 4. Open the URL it prints, create a free account or sign in, and come back. (Can't create an account? Skip this; only Lab 4 needs it.)

```
ollama signin
```

![Signing in to ollama.com](./images/ollama13.png?raw=true "Signing in to ollama.com")

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 2 - Choosing a model and customizing it**

**Purpose: See what the numbers on a model mean, compare speed between sizes, then build your own customized model with a Modelfile.**

1. Show both models' details. Compare *parameters*, *context length*, and *quantization*.

```
ollama show llama3.2:3b
```
```
ollama show llama3.2:1b
```

![Showing model details](./images/ollama14.png?raw=true "Showing model details")

<br><br>

2. Time the same one-sentence question on each model, small one first. Compare the `real` times.

```
time ollama run llama3.2:1b "What is a vector embedding? One sentence."
```
```
time ollama run llama3.2:3b "What is a vector embedding? One sentence."
```

![Comparing model sizes and speed](./images/ollama15.png?raw=true "Comparing model sizes and speed")

<br><br>

3. Look at the Modelfile behind Llama 3.2: the `FROM` line, the `TEMPLATE` block, and the `PARAMETER stop` lines. (What follows is license text.)

```
ollama show --modelfile llama3.2:3b | head -55
```

![Viewing a model's Modelfile](./images/ollama16.png?raw=true "Viewing a model's Modelfile")

<br><br>

4. Open the starter Modelfile - click [**modelfiles/Modelfile.shellcoach**](./modelfiles/Modelfile.shellcoach) or run the command below. Its three sections each hold a `TODO`; we fill them in next.

```
code modelfiles/Modelfile.shellcoach
```

![The skeleton Modelfile](./images/ollama17.png?raw=true "The skeleton Modelfile")

<br><br>

5. Merge in the completed version.

```
code -d extra/Modelfile-shellcoach-complete.txt modelfiles/Modelfile.shellcoach
```

   The left side is the complete file; the right side is your starter file. For each of the three change blocks, hover over the middle bar and click the arrow to copy the change across. A yellow bubble in the left margin means you can hover over that change for an explanation.

![Merging the completed Modelfile](./images/ollama50.png?raw=true "Merging the completed Modelfile")

   When done, click the X on the tab to close **and** save.

![Merging the completed Modelfile](./images/ollama54.png?raw=true "Merging the completed Modelfile")

<br><br>

6. Read what you merged: the `PARAMETER` defaults, the `SYSTEM` instructions, and the `MESSAGE` lines that give the model an example exchange.

<br><br>

7. Build the model (15 - 30 seconds), then confirm it's listed.

```
ollama create shellcoach -f modelfiles/Modelfile.shellcoach
```
```
ollama list
```

![Creating a custom model](./images/ollama19.png?raw=true "Creating a custom model")

<br><br>

8. Load `shellcoach` into memory.

```
python api/warmup.py shellcoach
```

<br><br>

9. Ask it a question. The command comes first, without you asking for that.

```
ollama run shellcoach "How do I find files modified in the last 24 hours?"
```

![Running the custom model](./images/ollama51.png?raw=true "Running the custom model")

<br><br>

10. Ask the base model the same question. Compare length, format, and whether the command came first.

```
ollama run llama3.2:3b "How do I find files modified in the last 24 hours?"
```

![Comparing custom model to base model](./images/ollama21.png?raw=true "Comparing custom model to base model")

<br><br>

11. Show `shellcoach`'s Modelfile. Ollama expanded your short file to over 200 lines.

```
ollama show --modelfile shellcoach
```

<br><br>

12. (Optional) Ask about a destructive command and watch the `CAUTION:` rule fire.

```
ollama run shellcoach "How do I delete every .tmp file under /var/log?"
```

   Then change `PARAMETER temperature 0.2` to `1.4`, save (CMD+S / Ctrl+S), rebuild, and run the same prompt three times. The answers vary more.

```
code modelfiles/Modelfile.shellcoach
```

![Changing temp](./images/ollama61.png?raw=true "Changing temp")

```
ollama create shellcoach -f modelfiles/Modelfile.shellcoach
```
```
ollama run shellcoach "How do I delete every .tmp file under /var/log?"
```

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 3 - Using Ollama from an application**

**Purpose: Use Ollama from code three ways - the raw web API with curl, the Python library, and a framework.**

1. Every command so far went through a local web service on port 11434. Check that it's running, then get the model list as JSON. (Output may start mid-line.)

```
curl http://localhost:11434
```
```
curl -sS http://localhost:11434/api/tags | python3 -m json.tool
```

![Listing models over the API](./images/ollama22.png?raw=true "Listing models over the API")

<br><br>

2. Call `/api/generate`: one prompt in, one answer out. `"stream": false` returns the answer as a single JSON object.

```
curl -sS http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "In two sentences, what is a REST API?",
  "stream": false,
  "options": { "temperature": 0.3, "num_predict": 60 }
}' | python3 -c "import sys,json; d=json.load(sys.stdin); d.pop('context',None); print(json.dumps(d,indent=2))"
```

   Find `eval_count` (tokens generated) and `total_duration` (nanoseconds). We remove the long `context` field before printing.

![Calling the generate endpoint](./images/ollama23.png?raw=true "Calling the generate endpoint")

<br><br>

3. Send the same request with streaming on, the default. The answer arrives as one small JSON object per token.

```
curl -sS http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "In two sentences, what is a REST API?",
  "options": { "num_predict": 60 }
}'
```

![Streaming responses](./images/ollama24.png?raw=true "Streaming responses")

<br><br>

4. `/api/chat` takes a list of messages instead of one prompt. Ask something it can't know. In the output, read the `"content"` of the `"message"`.

```
curl -sS http://localhost:11434/api/chat -d '{
  "model": "llama3.2:3b",
  "stream": false,
  "options": { "num_predict": 60 },
  "messages": [
    {"role": "system", "content": "You are terse and concrete."},
    {"role": "user", "content": "How much RAM does my server have?"}
  ]
}' | python3 -m json.tool
```

   Now send a conversation that already contains the answer. We write the model's earlier reply (`assistant`) ourselves.

```
curl -sS http://localhost:11434/api/chat -d '{
  "model": "llama3.2:3b",
  "stream": false,
  "options": { "num_predict": 60 },
  "messages": [
    {"role": "system", "content": "You are terse and concrete."},
    {"role": "user", "content": "My server has 6 GB of RAM and no GPU."},
    {"role": "assistant", "content": "Noted - 6 GB, CPU only."},
    {"role": "user", "content": "How much RAM does my server have?"}
  ]
}' | python3 -m json.tool
```

![The same question, cold and with history](./images/ollama25.png?raw=true "The same question, cold and with history")

   Now it answers 6 GB, and `prompt_eval_count` grows from about 39 to 71.

<br><br>

5. Ollama remembers nothing between requests. Any "memory" is your application resending the conversation - you'll write that code next.

<br><br>

6. Open the starter chat app - click [**api/chat_app.py**](./api/chat_app.py) or run the command below - and find the two `TODO` markers.

```
code api/chat_app.py
```

![The skeleton chat application](./images/ollama26.png?raw=true "The skeleton chat application")

<br><br>

7. Merge in the completed code the same way as in Lab 2, then click the X on the tab to close and save.

```
code -d extra/chat_app-complete.txt api/chat_app.py
```

![Merging the completed chat application](./images/ollama27.png?raw=true "Merging the completed chat application")

<br><br>

8. Read what you merged into `ask()`: the `ollama.chat()` call, the loop that prints each piece as it arrives, and `messages.append(...)`. That last line is the app's entire memory.

<br><br>

9. Run it. Ask the first question, then the follow-up, and watch `[history: N messages]` grow. Exit with CTRL-C.

```
python api/chat_app.py
```
```
What is the biggest downside of a 3-billion-parameter model?
```
```
How would I work around that?
```

![Multi-turn conversation with history](./images/ollama28.png?raw=true "Multi-turn conversation with history")


(You can use `Ctrl+C` to exit the application.)

<br><br>

10. (Optional) The same kind of chat through the LangChain framework. Open the code, then run it.

```
code api/simple_langchain.py
```
```
python api/simple_langchain.py "What is the capital of France?"
```

![Ollama through LangChain](./images/ollama30.png?raw=true "Ollama through LangChain")

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 4 - Cloud models and wiring Ollama into your tools**

**Purpose: Run a model far too large for this machine with the same commands and code, then start a real coding tool on Ollama with `ollama launch`.**

**Note: Cloud models are billed per token. If a step says you need credits, follow along on the instructor's screen.**

1. Check that you're signed in. If you aren't, it prints a URL to sign in or create a free account.

```
ollama signin
```

![Signed in to ollama.com](./images/ollama31.png?raw=true "Signed in to ollama.com")

<br><br>

2. Pull a cloud model. Nothing big downloads - the model runs on Ollama's servers. (If this name is gone, pick any model at https://ollama.com/search?c=cloud.)

```
ollama pull gpt-oss:120b-cloud
```

<br><br>

3. List your models. Compare the `SIZE` of the cloud model with `llama3.2:3b`.

```
ollama list
```

![A cloud model in the local list](./images/ollama32.png?raw=true "A cloud model in the local list")

<br><br>

4. Run it - 120 billion parameters, with the same `ollama run` command as before.

```
ollama run gpt-oss:120b-cloud "Compare a 3B local model with a 120B hosted model for a code review assistant. Be specific about where each one wins. Answer in under 120 words."
```

   The *Thinking...* block is the model working through the question first; adding `--hidethinking` hides it.

![Running a cloud-hosted model](./images/ollama33.png?raw=true "Running a cloud-hosted model")

<br><br>

5. Notice it answered faster than the local 3B did in Lab 2, and in more depth.

<br><br>

6. Check memory. The cloud model isn't loaded on this machine, so it doesn't appear.

```
ollama ps
```

<br><br>

7. Run the Lab 3 chat app against the cloud model by changing one environment variable. Ask the question, then exit with CTRL-C.

```
OLLAMA_MODEL=gpt-oss:120b-cloud python api/chat_app.py
```
```
In two sentences, what is a race condition?
```

![The same app against a cloud model](./images/ollama34.png?raw=true "The same app against a cloud model")

(You can use `Ctrl+C` to exit the application.)

<br><br>

8. See which developer tools `ollama launch` can set up and start for you.

```
ollama launch --help
```

![The launch command](./images/ollama35.png?raw=true "The launch command")

<br><br>

9. Start Claude Code (already installed in the codespace) on the cloud model. No Anthropic account or API key is needed.

```
ollama launch claude --model gpt-oss:120b-cloud
```

   The first launch asks a few setup questions: pick a theme, press Enter past the security notes, press ESC to skip terminal setup, then choose **Yes, I trust this folder**. If a *Welcome to Claude Code for VS Code* panel appears, press Enter.

![Claude Code running on an Ollama model](./images/ollama36.png?raw=true "Claude Code running on an Ollama model")

   The box on the left names the model. Exit with `/exit`, then try the small local model:

```
ollama launch claude --model llama3.2:3b
```

   Ollama warns that this model is too small to drive a coding agent. Press ESC to back out.

![The agent-capability gate](./images/ollama37.png?raw=true "The agent-capability gate")

<br><br>

10. (Optional) Check your cloud usage at https://ollama.com/settings/usage, or sign out.

```
ollama signout
```

<p align="center">
**[END OF LAB]**
</p>
</br></br>

<br>

<p align="center">
<b>PART TWO - TAKE-HOME LAB</b>
</p>

<p align="center">
<i>These go deeper on material the slides cover. Nothing here is required for the in-class session.</i>
</p>

<br>

**Lab 5 - Structured output, OpenAI compatibility, and the troubleshooting toolkit**

**Purpose: Get JSON you can rely on, run OpenAI code against Ollama, and learn the commands to use when something breaks.**

**Models stay loaded in this codespace, so there is nothing to warm up.**

1. With structured output, you send a JSON Schema and the answer must match it. Open the script and look at `SCHEMA`. `maxItems` keeps the `used_for` list from growing without end.

```
code api/structured_output.py
```

![Schema and format](./images/ollama55.png?raw=true "Schema and format")

<br><br>

2. Run it, then run it again with another real subject. The shape stays the same; the content changes.

```
python api/structured_output.py PostgreSQL
```

![Structured JSON output](./images/ollama38.png?raw=true "Structured JSON output")

<br><br>

3. Now try a product that doesn't exist. The schema forces a complete answer anyway - it guarantees the shape, not the truth.

```
python api/structured_output.py Fluxdash
```

![A confident answer about a product that does not exist](./images/ollama41.png?raw=true "A confident answer about a product that does not exist")

<br><br>

4. (Optional) Add `"maintained_by": {"type": "string"},` to `SCHEMA`, save (CMD+S / Ctrl+S), and rerun.

```
code api/structured_output.py
```

![Updated schema](./images/ollama56.png?raw=true "Updated schema")

```
python api/structured_output.py PostgreSQL
```

![Updated schema run](./images/ollama62.png?raw=true "Updated schema run")

<br><br>

5. Ollama also answers OpenAI-style requests at `/v1`. List the models there.

```
curl -sS http://localhost:11434/v1/models | python3 -m json.tool
```

![The OpenAI-compatible model list](./images/ollama39.png?raw=true "The OpenAI-compatible model list")

<br><br>

6. This script uses OpenAI's own Python library, pointed at your local server. Only the address and the model name change; the `api_key` can be any text.

```
code api/openai_compat.py
```

![OpenAI Use](./images/ollama58.png?raw=true "OpenAI Use")

```
python api/openai_compat.py
```

![OpenAI SDK against local Ollama](./images/ollama40.png?raw=true "OpenAI SDK against local Ollama")

<br><br>

7. (Optional) Reach Ollama's cloud directly with an API key, as you would from a server. Create a key at https://ollama.com/settings/keys, then run the script. Without a key it goes through your local server, which works if you finished Lab 4.

```
export OLLAMA_API_KEY=your_key_here
```
```
code api/cloud_chat.py
```
```
python api/cloud_chat.py
```

![Running cloud chat with key](./images/ollama59.png?raw=true "Running cloud chat with key")

<br><br>

8. When something breaks, first check whether the service is up, then read its log.

```
curl -sS http://localhost:11434/api/tags > /dev/null && echo "Ollama is up" || echo "Ollama is NOT running"
```
```
tail -30 /tmp/ollama.log
```

![Running cloud chat with key](./images/ollama60.png?raw=true "Running cloud chat with key")

<br><br>

9. If you ever see `address already in use` on port 11434, stop Ollama and start it again.

```
bash scripts/shutdown_ollama.sh
```
```
bash scripts/startOllama.sh
```

<br><br>

10. Remove a model you no longer need.

```
ollama list
```
```
ollama rm shellcoach
```

<br><br>

**Where to go next**

   - Browse https://ollama.com/search and filter by what a model can do (`tools`, `vision`, `embedding`, `thinking`)
   - Pull an embedding model, call `/api/embed`, and build a small search-your-documents prototype offline
   - Use `/api/chat` with the `tools` parameter to let a local model call your functions
   - Point LangChain or LlamaIndex at your local server
   - Read the API reference at https://docs.ollama.com

<p align="center">
**[END OF LAB]**
</p>
</br></br>

</br></br>
<p align="center">
**THANKS!**
</p>

</br></br>
<p align="center">
<b>For educational use only by the attendees of our workshops.</b>
</p>
<p align="center">
<b>(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.</b>
</p>
