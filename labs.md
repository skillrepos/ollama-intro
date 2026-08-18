# Getting Started with Ollama
## Running and using local LLMs 
## Session labs
## Revision 6.7 - 08/18/26

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

**NOTE: To copy and paste in the codespace, you may need to use keyboard commands - CTRL-C and CTRL-V. Chrome may work best for this.**

**NOTE: Unless a step says otherwise, run every command from the root of the repository. You can always get back there with `cd /workspaces/ollama-intro`.**

**NOTE: This is a CPU-only codespace. Short answers from our default `llama3.2:3b` model will come back in about 4 - 6 seconds once the model is warm; long answers can take 30 seconds or more, because time scales with answer length. That is normal. Lab 1 step 3 warms the models up so you don't pay a load penalty on top of it.**

<br><br>

**Lab guide**

| Lab | Steps | Time | When |
| :-- | :-- | :-- | :-- |
| 1 - Running your first local model | 12 | 10 min | In class |
| 2 - Choosing a model and customizing it | 12 | 12 min | In class |
| 3 - Using Ollama from an application | 10 | 12 min | In class |
| 4 - Cloud models and wiring up your tools | 11 | 9 min | In class |
| | | | |
| 5 - Structured output, OpenAI compatibility, and troubleshooting | 10 | 10 min | Take-home |

**Labs 1 - 4 are in-class.** Lab 5 is optional if we have time or you can do it later. It covers two developer features we likely won't have time to try and troubleshooting commands you'll want when you are working on your own.

**Lab 4 needs a free ollama.com account.** Creating one takes about a minute. Lab 1 ends with the step. **Just run it before you reach Lab 4** (in a live session). **Signin must be run from the codespace terminal.**

Steps marked **(Optional)** inside a lab are there for people who finish early. 

<br><br>

<p align="center">
<b>PART ONE - IN-CLASS LABS</b>
</p>

<br>

**Lab 1 - Running your first local model**

**Purpose: In this lab, we'll warm up the models, run one locally, and learn the interactive session commands.**

1. Let's start by confirming Ollama is installed and which version we have. Go to the *TERMINAL* tab in the bottom part of your codespace and enter the command below.

```
ollama --version
```

![Checking the Ollama version](./images/ollama5.png?raw=true "Checking the Ollama version")

<br><br>

2. Look at what models are on the disk with the first command. 

```
ollama list
```

Now add a second model (the 1B Llama 3.2) next to the 3B one we already have.

```
ollama pull llama3.2:1b
```

Check to see that both are shown.

```
ollama list
```

![Listing installed models](./images/ollama7.png?raw=true "Listing installed models")

<br><br>

3. Let's "warm up" both models now, so no later step pays the performance penalty of reading weights off disk.

```
python api/warmup.py
```

![Warming up the models](./images/ollama6.png?raw=true "Warming up the models")

   **If that command reports it could not reach Ollama**, the background service is not running. Start it with `bash scripts/startOllama.sh` and try again.

<br><br>

4. Start an interactive session with our default model, the 3-billion-parameter Llama 3.2.

```
ollama run llama3.2:3b
```

<br><br>

5. You should now be at a `>>>` prompt. Ask it something, then ask a follow-up that only makes sense in context.

```
In two sentences, what is the difference between a model and a checkpoint?
```
```
Why does that matter to a developer? Two sentences.
```

![First prompts to a local model](./images/ollama8.png?raw=true "First prompts to a local model")

<br><br>

6. The `>>>` prompt has its own set of commands, all starting with a `/`. Let's see them, then look at what this model actually is.

```
/?
```
```
/show info
```

![Model info from inside a session](./images/ollama9.png?raw=true "Model info from inside a session")

<br><br>

7. Let's look at **`num_predict`**. That one is a hard cap on how many tokens an answer may run to. Set it very low and ask a question that would normally get a long answer.

```
/set parameter num_predict 20
```
```
Explain what a container image is.
```

   The answer stops mid-sentence. Raise the cap and ask again - `/clear` wipes the conversation but *keeps* your parameter setting.

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

8. Exit the session. `/bye` is the way out - typing "quit" or "exit" just sends those words to the model as a prompt.

```
/bye
```

<br><br>

9. Leaving the session did **not** unload the model - running the `ps` command shows what is still in memory, and when it will be released. Run the command.

```
ollama ps
```

![Models currently loaded in memory](./images/ollama11.png?raw=true "Models currently loaded in memory")

<br><br>

10. Passing a prompt directly on the command line runs it once and exits - this is how you'd use Ollama in a script.

```
ollama run llama3.2:3b "List three reasons to run an LLM locally. One short line each."
```

![One-shot prompt from the command line](./images/ollama12.png?raw=true "One-shot prompt from the command line")

<br><br>

11. (Optional) It reads standard input too, so it pipes like any other command.

```
cat requirements.txt | ollama run llama3.2:3b "What is this dependency file for? Two sentences."
```

<br><br>

12. From the codespace terminal, sign in so you are ready for Lab 4. The command prints a URL - open it, create a free account or sign in, and come back. (Skip this if you cannot create an account; Lab 4 is the only lab that needs one.)

```
ollama signin
```

![Signing in to ollama.com](./images/ollama13.png?raw=true "Signing in to ollama.com")

<br><br>

**What just happened**

- **`ollama pull` is the command you'll use most outside this workshop.** Models are stored as shared layers, so a second tag of something you already have downloads only the difference.
- **The slowest prompt you ever send is the first one** - the weights have to be read off disk first. `api/warmup.py` pays that once; it is four lines of HTTP that you'll write by hand in Lab 3.
- **`ollama list` shows what is on disk; `ollama ps` shows what is in memory.** Different questions. The *SIZE* column is a good first proxy for how much memory a model wants.
- **`num_predict` is a hard stop, not a request for brevity.** The model never wraps up early - generation just halts. Your 200-token answer is very likely cut off too, just further along. For short *and* complete, ask for brevity in the prompt and keep the cap as a safety net.
- **The interactive session is stateful; the server is not.** The CLI is holding your conversation and resending it every turn - which is what Lab 3 has you do yourself, in code. We'll bake `num_predict` and `temperature` into a model of our own in Lab 2.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 2 - Choosing a model and customizing it**

**Purpose: In this lab, we'll see what the numbers on a model actually mean, feel the size-versus-speed tradeoff first hand, then build our own customized model with a Modelfile.**

1. The same model info is available from the shell. Compare the *Model* blocks - *parameters*, *context length*, and *quantization*.

```
ollama show llama3.2:3b
```
```
ollama show llama3.2:1b
```

![Showing model details](./images/ollama14.png?raw=true "Showing model details")

<br><br>

2. Now let's feel that difference. Both models are warm, so you're timing generation - run the small one first and compare the `real` times.

```
time ollama run llama3.2:1b "What is a vector embedding? One sentence."
```
```
time ollama run llama3.2:3b "What is a vector embedding? One sentence."
```

![Comparing model sizes and speed](./images/ollama15.png?raw=true "Comparing model sizes and speed")

<br><br>

3. Every model has a Modelfile behind it, even downloaded ones. Look at the recipe for Llama 3.2 - the `FROM` line, the `TEMPLATE` block, the `PARAMETER stop` values.

```
ollama show --modelfile llama3.2:3b | head -55
```

   The rest is the Llama 3.2 license text - drop the `| head -55` to see all of it.

![Viewing a model's Modelfile](./images/ollama16.png?raw=true "Viewing a model's Modelfile")

<br><br>

4. We've started a Modelfile for you and left the interesting parts out. Open it by clicking [**modelfiles/Modelfile.shellcoach**](./modelfiles/Modelfile.shellcoach) or with the command below.

```
code modelfiles/Modelfile.shellcoach
```

   Three labeled sections each hold a `TODO`. **This file is incomplete; we merge in the working version next.**

![The skeleton Modelfile](./images/ollama17.png?raw=true "The skeleton Modelfile")

<br><br>

5. Fill in the gaps by merging in the completed version by running the command below.

```
code -d extra/Modelfile-shellcoach-complete.txt modelfiles/Modelfile.shellcoach
```

   You'll get a side-by-side view with **three change blocks**, one per labeled section. The left side is the complete code. The right side is the starter code. We will build out the starter code by merging in the changes from the left. Review the code in red on the left, then, when ready, hover over the middle bar (between the views) and click on the arrow that shows up to do the merge. Also, if you see a yellow bubble in the left "gutter", that means if you hover over the code change, you'll get a pop-up further explaining the change. 
   
![Merging the completed Modelfile](./images/ollama50.png?raw=true "Merging the completed Modelfile")

When done merging, click on the X at the top to close **and** save the merged version.

![Merging the completed Modelfile](./images/ollama54.png?raw=true "Merging the completed Modelfile")

<br><br>

6. Read through what you merged: the `PARAMETER` defaults, the `SYSTEM` persona and rules, and the `MESSAGE` lines that seed a fake exchange. The `FROM llama3.2:3b` pins it to a base model - that is what makes it reproducible.

<br><br>

7. Build the model, then confirm it exists. This takes 15-30 seconds - it isn't retraining, just layering our instructions on existing weights.

```
ollama create shellcoach -f modelfiles/Modelfile.shellcoach
```
```
ollama list
```

![Creating a custom model](./images/ollama19.png?raw=true "Creating a custom model")

<br><br>

8. Warm `shellcoach` up with the same program, this time passing a model name.

```
python api/warmup.py shellcoach
```

<br><br>

9. Try it. Notice you don't have to tell it how to answer - the format is baked in.

```
ollama run shellcoach "How do I find files modified in the last 24 hours?"
```

![Running the custom model](./images/ollama51.png?raw=true "Running the custom model")

<br><br>

10. For contrast, ask the *base* model the same question. Compare length, format, and whether the command came first.

```
ollama run llama3.2:3b "How do I find files modified in the last 24 hours?"
```

![Comparing custom model to base model](./images/ollama21.png?raw=true "Comparing custom model to base model")

<br><br>

11. Our model has its own Modelfile now too - but it is *not* the tidy file you wrote. Ollama expanded it to over 200 lines.

```
ollama show --modelfile shellcoach
```

<br><br>

12. (Optional) Two things to try if you finish early.

   First, hand it a genuinely destructive command and watch the safety rule fire.

```
ollama run shellcoach "How do I delete every .tmp file under /var/log?"
```

   Then take the guard rails off: change `PARAMETER temperature 0.2` to `1.4`, save, rebuild, and rerun a few times - the answers will vary.

```
code modelfiles/Modelfile.shellcoach
```
```
ollama create shellcoach -f modelfiles/Modelfile.shellcoach
```
```
ollama run shellcoach "How do I delete every .tmp file under /var/log?"
```

<br><br>

**What just happened**

- **Parameters, context length, and quantization are most of model selection.** Parameters are roughly capability and memory appetite, context length is how much text the model considers at once, and quantization is precision traded for size - `Q4_K_M` is about 4 bits per weight.
- **Quantization matters as much as parameter count.** The 3B ran 30-60% slower than the 1B, not 3x: on CPU, speed follows bytes read per token, and 3.2B x 4 bits against 1.2B x 8 bits is only ~1.3x the bytes. No ranking here, only a choice.
- **`SYSTEM` is prepended to every conversation; `MESSAGE` seeds a fake one.** That few-shot priming is where shellcoach's command-first code block comes from, and `num_predict 160` is why it stops while the base model rambles.
- **Customization buys behavior, not knowledge.** Same weights underneath, so a mistake the base model makes (watch the `find -mtime` sign) shellcoach makes too. The `CAUTION:` rule fires on judgement and sometimes flags a harmless command.
- **A customized model costs a Modelfile, not memory.** `shellcoach` shares blobs with `llama3.2:3b`, so `ollama ps` shows no separate entry. Share your few-line `Modelfile.shellcoach`, not the 200-line expansion.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 3 - Using Ollama from an application**

**Purpose: In this lab, we'll work through the three developer-facing ways into Ollama - the raw HTTP API with curl, the official Python library, and a framework - and see that all three hit the same endpoint.**

1. Everything so far went through a local HTTP service on port 11434. Run some commands to see output from accessing that service. The first command returns `Ollama is running`; the second gives you `ollama list` as JSON your code could consume. (NOTE: Output may be at the beginning of a line.)

```
curl http://localhost:11434
```
```
curl -sS http://localhost:11434/api/tags | python3 -m json.tool
```

![Listing models over the API](./images/ollama22.png?raw=true "Listing models over the API")

<br><br>


2. `/api/generate` is the single-turn endpoint - one prompt in, one completion out, with `"stream": false` asking for one complete JSON object rather than a stream of fragments. Use the `curl` command below to call the API with the prompt `In two sentences, what is a REST API?`.

```
curl -sS http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "In two sentences, what is a REST API?",
  "stream": false,
  "options": { "temperature": 0.3, "num_predict": 60 }
}' | python3 -c "import sys,json; d=json.load(sys.stdin); d.pop('context',None); print(json.dumps(d,indent=2))"
```

   (We drop the `context` field before printing - a few hundred token IDs that would bury everything else.)

![Calling the generate endpoint](./images/ollama23.png?raw=true "Calling the generate endpoint")

<br><br>

3. Now issue the same request with streaming left on, which is the default. Note the difference from the last run.

```
curl -sS http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "In two sentences, what is a REST API?",
  "options": { "num_predict": 60 }
}'
```

![Streaming responses](./images/ollama24.png?raw=true "Streaming responses")

<br><br>

4. The `/api/generate` endpoint we were using has no memory. Another endpoint, `/api/chat`, takes a *messages* array instead which serves as "memory". Let's ask the **same question twice**, once cold and once with a conversation in front of it.

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

   It cannot answer because it doesn't have access to the information. Let's pretend though that we had already gotten an answer from the model (the `assistant`) and put those details in the array, writing the `assistant` turn ourselves. This simulates building up a set of messages (the `memory`) over time.

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

   Now it answers: 6 GB. The only thing that changed is the `messages` array, and `prompt_eval_count` goes from roughly 39 to 71.

<br><br>

5. That's the key mental model for the rest of the lab: **Ollama is stateless.** Any "memory" in an application is something your application is doing - we're about to write that code.

<br><br>

6. The official Python library is a thin, typed wrapper over those same endpoints. Let's build an example. Open the starter code for a chat application we've provided - click [**api/chat_app.py**](./api/chat_app.py) or use the command below - and find the two `TODO` markers.

```
code api/chat_app.py
```


![The skeleton chat application](./images/ollama26.png?raw=true "The skeleton chat application")

<br><br>

7. As before, we'll build out the code with the "diff and merge" approach. Run the command below.,
```
code -d extra/chat_app-complete.txt api/chat_app.py
```

   Review and merge in the completed code, then close and save your changes by clicking on the `X` in the tab at the top of the diff view.

![Merging the completed chat application](./images/ollama27.png?raw=true "Merging the completed chat application")

<br><br>

8. Look at what you merged into `ask()`: the `ollama.chat()` call, the `stream=True` loop that prints each chunk as it arrives, and `messages.append({"role": "assistant", ...})`. **That last line is the entire "memory" of this application.**

<br><br>

9. Now run it. Ask the first question below, then the follow-up - which has no meaning on its own. Watch the `[history: N messages]` counter grow after each turn, then exit with CTRL-C.

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

<br><br>


10. (Optional if time allows.) This code shows using an external framework `langchain-ollama` to do the same example. Open and review the code and then run it.

```
code api/simple_langchain.py
```
```
python api/simple_langchain.py "What is the capital of France?"
```

![Ollama through LangChain](./images/ollama30.png?raw=true "Ollama through LangChain")

<br><br>

**What just happened**

- **The JSON around the `response` field is how you measure a model on your own task**, instead of guessing from a leaderboard. `eval_count` is tokens generated, `eval_duration` is nanoseconds spent generating, and `total_duration` covers the whole request.
- **Streaming is what makes a chat UI feel responsive** - one JSON object per token, ending with `done: true`. On a CPU-only box it is the difference between usable and apparently broken.
- **The `messages` array is a transcript you hand over, not a record of what happened.** You wrote the `assistant` turn and the model accepted it. Only the *last* message is answered; everything before it is context.
- **Every "the AI knows about my project" feature works the way step 4 did.** Nobody trained a model on your data - something assembled an array like yours and resent it on every request. Those extra `prompt_eval_count` tokens *are* the memory, and why long chats get slower.
- **All three layers hit the same endpoint.** `ChatOllama` sets the same options you typed by hand and sends the same roles you sent to `/api/chat`, adding no memory of its own. A framework buys one interface across many providers; it costs a dependency and a layer to debug through.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 4 - Cloud models and wiring Ollama into your tools**

**Purpose: In this lab, we'll run a model far too large for this machine with the same commands and code, then point a real coding tool at Ollama with `ollama launch`.**

**Note: this lab needs a free ollama.com account. If you ran the signin step at the end of Lab 1 you can skip step 1; if not, step 1 handles it.**

1. Ollama Cloud runs large models on Ollama's hardware, behind the API you have been using. If you signed in at the end of Lab 1 this says so; otherwise it prints a URL to create a free account.

```
ollama signin
```

![Signed in to ollama.com](./images/ollama31.png?raw=true "Signed in to ollama.com")

<br><br>

2. Let's pull a cloud model to get it in our list of available models. Cloud models carry a `-cloud` tag, and pulling one downloads no weights at all.

   **Cloud model names change frequently. If the name below is gone, open https://ollama.com/search?c=cloud and substitute any model whose tag ends in `-cloud`.**

```
ollama pull gpt-oss:120b-cloud
```

<br><br>

3. Confirm what just landed - compare the `SIZE` column for the cloud model against `llama3.2:3b`.

```
ollama list
```

![A cloud model in the local list](./images/ollama32.png?raw=true "A cloud model in the local list")

<br><br>

4. Now run it - a 120-billion-parameter model, impossible to fit in this codespace. Note the command is identical to every other `ollama run` you have typed today.

```
ollama run gpt-oss:120b-cloud "Compare a 3B local model with a 120B hosted model for a code review assistant. Be specific about where each one wins. Answer in under 120 words."
```

   (The word limit matters - unbounded, this model writes two screens of tables.)

![Running a cloud-hosted model](./images/ollama33.png?raw=true "Running a cloud-hosted model")

<br><br>

5. It arrived **faster** than your local 3B despite being forty times larger - about 3 seconds against 14 - and is visibly better reasoned.

<br><br>

6. Check what this cost you locally - nothing is loaded, so the cloud model does not appear.

```
ollama ps
```

<br><br>

7. Now a key part: **your code does not change either.** The Lab 3 chat app reads its model from an environment variable. Use the single command below to point it at the cloud model.  Then you can query it and get the response from the same code referencing the larger, faster model. When done, exit with CTRL-C.

```
OLLAMA_MODEL=gpt-oss:120b-cloud python api/chat_app.py
```

![The same app against a cloud model](./images/ollama34.png?raw=true "The same app against a cloud model")

<br><br>

8. Here's one more cool and useful feature. `ollama launch` configures and starts real developer tools against your models - no environment variables, no config files. See what it supports.

```
ollama launch --help
```

![The launch command](./images/ollama35.png?raw=true "The launch command")

<br><br>

9. Now actually launch one. **Claude Code is already installed here**, so a real coding agent starts - no Anthropic account, no API key.

```
ollama launch claude --model gpt-oss:120b-cloud
```

   **First launch runs Claude Code's own setup:** theme, Enter past the security notes, ESC past the terminal-setup offer, then **"Yes, I trust this folder"** - none of it an Anthropic login.

![Claude Code running on an Ollama model](./images/ollama36.png?raw=true "Claude Code running on an Ollama model")

   The box on the left names the model it is driving. Exit with `/exit`.

   Now try the small local model:

```
ollama launch claude --model llama3.2:3b
```

   It is a **warning, not a hard refusal** - press ESC to back out.

![The agent-capability gate](./images/ollama37.png?raw=true "The agent-capability gate")

<br><br>

10. (Optional) The free tier covers light usage with limits that reset on a rolling window; everything else here runs locally at zero cost. Check usage at https://ollama.com/settings.  You can also sign out if you want with the command below.

```
ollama signout
```

<br><br>

**What just happened**

- **A `-cloud` tag registers a route, not weights.** Nothing landed on your disk and `ollama ps` stayed empty for it - your machine only forwarded the request to someone else's GPUs. The trade is your prompt leaving the machine.
- **Local and hosted are one line apart** - same library, same call, same streaming loop, same history, only the model name changed. That is the argument for building against Ollama's API rather than a vendor SDK.
- **`ollama launch` gates on the model, not the tool.** Driving an agent needs reliable tool calling, not just good prose - and an agent makes several round trips per question, the one thing that could eat your free tier.

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

**Purpose: In this lab, we'll use structured output to get JSON you can rely on, run existing OpenAI code against Ollama unchanged, and finish with the handful of commands worth knowing when something breaks.**

**Nothing to warm up.** This codespace pins models in memory (`OLLAMA_KEEP_ALIVE=-1`), so they are loaded and ready whenever you come back to this lab.

1. **Structured output** hands Ollama a JSON Schema in the `format` field and the reply is constrained to match. Open the script and look at the `SCHEMA` object.

```
code api/structured_output.py
```

![Schema and format](./images/ollama55.png?raw=true "Schema and format")

<br><br>

2. Run it. The raw response prints first, then the same thing after `json.loads()` - guaranteed to succeed because of the schema. Run it again with another real subject and watch the *shape* stay identical while the content changes.

```
python api/structured_output.py PostgreSQL
```

![Structured JSON output](./images/ollama38.png?raw=true "Structured JSON output")

<br><br>

3. **The schema guarantees the shape, not the truth.** Invent a product that does not exist - mash two tech-sounding words together - and the `required` fields mean the model **must** fill in a category, a release year, and use cases.

```
python api/structured_output.py Fluxdash
```

![A confident answer about a product that does not exist](./images/ollama41.png?raw=true "A confident answer about a product that does not exist")

<br><br>

4. (Optional) Open `api/structured_output.py` and add a new property to `SCHEMA` - for example `"maintained_by": {"type": "string"}` - then rerun and see the model fill it in. (After you make the change, don't forget to save it with `CMD+S` or `CTRL+S`.)

```
code api/structured_output.py
```
```
python api/structured_output.py PostgreSQL
```

![Updated schema](./images/ollama56.png?raw=true "Updated schema")

<br><br>

5. Ollama also serves an **OpenAI-compatible** surface at `/v1`. Confirm the endpoint is there.

```
curl -sS http://localhost:11434/v1/models | python3 -m json.tool
```

![The OpenAI-compatible model list](./images/ollama39.png?raw=true "The OpenAI-compatible model list")

<br><br>

6. This script uses the *official OpenAI Python SDK* - not the Ollama library - pointed at your local server. The `api_key` is required by the SDK but ignored by Ollama, so any string works.

```
code api/openai_compat.py
```

![OpenAI Use](./images/ollama58.png?raw=true "OpenAI Use")

```
python api/openai_compat.py
```

![OpenAI SDK against local Ollama](./images/ollama40.png?raw=true "OpenAI SDK against local Ollama")

<br><br>

7. (Optional) A second route to Ollama Cloud: an API key against `https://ollama.com` directly, which is what you'd do from a server or a CI job. Create a key at https://ollama.com/settings/keys, then run the script - with no key it fails with a checklist of what is missing.

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

8. Finally, here's some troubleshooting tips. The first two questions that usually occur when something breaks: is the service even up, and if not, why?  Here's how to get the answers to those.

```
curl -sS http://localhost:11434/api/tags > /dev/null && echo "Ollama is up" || echo "Ollama is NOT running"
```
```
tail -30 /tmp/ollama.log
```

![Running cloud chat with key](./images/ollama60.png?raw=true "Running cloud chat with key")

<br><br>

9. If you ever get `address already in use` on port 11434, there's a stale server - stop everything, then start it cleanly.

```
bash scripts/shutdown_ollama.sh
```
```
bash scripts/startOllama.sh
```

<br><br>

10. Done experimenting? Reclaim disk from models you no longer need.

```
ollama list
```
```
ollama rm shellcoach
```

<br><br>

**What just happened**

- **Constrained output can force a confident answer where the honest one is "never heard of it."** The schema validates shape; truth is your job. Give the model a way out - a `"known": {"type": "boolean"}` field, or an `"unknown"` enum option - when you care about the difference.
- **`/v1` means most OpenAI code works by changing two things:** the base URL and the model name. Develop free and private against localhost, then point `base_url` at a hosted provider to ship.
- **A "slow first prompt" is almost never a bug.** This codespace sets `OLLAMA_KEEP_ALIVE=-1`, which is why `ollama ps` says *Forever*. On your own machine the default is five minutes, after which the next prompt pays a reload.
- **`keep_alive` is a JSON number you set per request:** `-1` pins a model, `0` unloads it on completion. A quoted `"-1"` is read as a duration, has no unit, and is rejected - `"30m"` and `"1h"` are the string forms. `ollama stop <model>` unloads one now.

**Where to go next**

   - Browse https://ollama.com/search - filter by capability (`tools`, `vision`, `embedding`, `thinking`), and check four things: does it fit in RAM, can it do your task, is the context window big enough, is the license OK
   - Pull an embedding model, call `/api/embed`, and build a small RAG prototype entirely offline
   - Use `/api/chat` with the `tools` parameter to try local tool calling
   - Run `ollama launch` for real, on a machine where your coding tool is installed
   - Point LangChain or LlamaIndex at your local server - both have native Ollama providers
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
