# Getting Started with Ollama
## Running and using local LLMs - two-hour workshop
## Session labs
## Revision 3.1 - 08/07/26

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

**NOTE: To copy and paste in the codespace, you may need to use keyboard commands - CTRL-C and CTRL-V. Chrome may work best for this.**

**NOTE: Unless a step says otherwise, run every command from the root of the repository. You can always get back there with `cd /workspaces/ollama-intro`.**

**NOTE: This is a CPU-only codespace. Prompts take time - expect 20 to 60 seconds for an answer from our default `llama3.2:3b`. That is normal, not broken. Lab 1 step 2 warms the models up so you don't pay a load penalty on top of it.**

<br><br>

**Lab guide**

| Lab | Steps | Time | When |
| :-- | :-- | :-- | :-- |
| 1 - Running your first local model | 12 | 10 min | In class |
| 2 - Choosing a model and customizing it | 12 | 12 min | In class |
| 3 - Using Ollama from an application | 12 | 12 min | In class |
| 4 - Cloud models and wiring up your tools | 11 | 9 min | In class |
| | | | |
| 5 - Managing models on disk and in memory | 10 | 10 min | Take-home |
| 6 - The REST API in depth | 8 | 10 min | Take-home |
| 7 - Troubleshooting toolkit | 11 | 8 min | Take-home |

**Labs 1 - 4 are what we do together in the session.** Labs 5 - 7 are written to the same standard and are yours to work through afterward - they go deeper on material the slides cover but the clock does not allow us to type through.

**Lab 4 needs a free ollama.com account.** Creating one takes about a minute. Lab 1 ends with an optional step that gets you signed in early - **do it during the break** and Lab 4 will go much faster.

Steps marked **(Optional)** inside a lab are there for people who finish early. Skip them if the room is moving on.

<br><br>

<p align="center">
<b>PART ONE - IN-CLASS LABS</b>
</p>

<br>

**Lab 1 - Running your first local model**

**Purpose: In this lab, we'll warm up the models, run one locally, and learn the interactive session commands. (approx. 10 minutes)**

1. Let's start by confirming Ollama is installed and which version we have. Go to the *TERMINAL* tab in the bottom part of your codespace and enter the command below.

```
ollama --version
```

![Checking the Ollama version](./images/ollama5.png?raw=true "Checking the Ollama version")

<br><br>

2. Now let's warm up. The slowest prompt you will ever send is the first one, because the model weights have to be read off disk into memory before a single token comes back. The program below pays that cost once, up front, for both workshop models - so no lab step has to. Run it and watch the load times.

```
python api/warmup.py
```

![Warming up the models](./images/ollama6.png?raw=true "Warming up the models")

   Those seconds are now *not* charged to your first real prompt. We'll look at how this program works in Lab 3 - it is four lines of HTTP.

   **If that command reports it could not reach Ollama**, the background service is not running. Start it with `bash scripts/startOllama.sh` and try again.

<br><br>

3. Now let's see what models are already installed. Notice the *NAME*, *ID*, *SIZE*, and *MODIFIED* columns. The size shown is the size on disk, which is a good first proxy for how much memory the model will want.

```
ollama list
```

![Listing installed models](./images/ollama7.png?raw=true "Listing installed models")

<br><br>

4. Let's run one. The command below starts an interactive session with the 3-billion-parameter Llama 3.2 model - our default for the workshop. Because we warmed it up in step 2, it should come back at the `>>>` prompt almost immediately.

```
ollama run llama3.2:3b
```

<br><br>

5. You should now be at a `>>>` prompt. Ask it something, wait for the answer, then ask a follow-up that only makes sense in context - this is a real chat session and it remembers what you just said.

```
In two sentences, what is the difference between a model and a checkpoint?
```
```
Why does that matter to a developer? Two sentences.
```

![First prompts to a local model](./images/ollama8.png?raw=true "First prompts to a local model")

<br><br>

6. The `>>>` prompt has its own set of commands, all starting with a `/`. Let's see them, then look at what this model actually is - architecture, parameter count, quantization, and context length.

```
/?
```
```
/show info
```

![Model info from inside a session](./images/ollama9.png?raw=true "Model info from inside a session")

<br><br>

7. We can also change how the model behaves without leaving the session. *Temperature* controls randomness - low values are more deterministic and repetitive, high values are more varied and more likely to wander. Run all four commands below in order and compare the two sets of answers.

```
/set parameter temperature 0.1
```
```
Three names for a coffee shop. Just the names.
```
```
/set parameter temperature 1.5
```
```
Three names for a coffee shop. Just the names.
```

![Comparing temperature settings](./images/ollama10.png?raw=true "Comparing temperature settings")

   This is the single most useful knob you have, and we'll bake a value for it into our own model in Lab 2.

<br><br>

8. Let's exit the session. Note that `/bye` is the way out - typing "quit" or "exit" just sends those words to the model as a prompt.

```
/bye
```

<br><br>

9. Back at the shell prompt, notice that leaving the session did **not** unload the model. The command below shows what is currently loaded in memory and when it will be released.

```
ollama ps
```

![Models currently loaded in memory](./images/ollama11.png?raw=true "Models currently loaded in memory")

<br><br>

10. You don't have to use interactive mode at all. Passing a prompt directly on the command line runs it once and exits - this is how you'd use Ollama in a script.

```
ollama run llama3.2:3b "List three reasons to run an LLM locally. One short line each."
```

![One-shot prompt from the command line](./images/ollama12.png?raw=true "One-shot prompt from the command line")

<br><br>

11. (Optional) Because it reads standard input, it composes with the rest of your shell like any other command. Try piping a file into it.

```
cat requirements.txt | ollama run llama3.2:3b "What is this dependency file for? Two sentences."
```

<br><br>

12. **(Optional - but please do this during the break.)** Lab 4 uses a cloud-hosted model, which needs a free ollama.com account. Getting signed in now means Lab 4 starts on the interesting part instead of on a signup form. Run the command below; it prints a URL. Open it, create a free account or sign in, and come back.

```
ollama signin
```

![Signing in to ollama.com](./images/ollama13.png?raw=true "Signing in to ollama.com")

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 2 - Choosing a model and customizing it**

**Purpose: In this lab, we'll see what the numbers on a model actually mean, feel the size-versus-speed tradeoff first hand, then build our own customized model with a Modelfile. (approx. 12 minutes)**

1. In Lab 1 we saw model info from inside a session. The same thing is available from the shell. Run both commands below and compare the *Model* blocks - specifically *parameters*, *context length*, and *quantization*.

```
ollama show llama3.2:3b
```
```
ollama show llama3.2:1b
```

![Showing model details](./images/ollama14.png?raw=true "Showing model details")

   Those three values are most of what you need for model selection:
   - **parameters** - roughly how capable the model is, and roughly how much memory it needs
   - **context length** - how much text it can consider at once (prompt + history + answer)
   - **quantization** - how much precision was traded away to shrink it (`Q4_K_M` means about 4 bits per weight)

<br><br>

2. Now let's feel that difference rather than just read it. We'll ask both models the same question and time each one. Both are already warm from Lab 1, so what you're timing is generation, not loading. Run the small one first, then the large one, and compare the `real` times.

```
time ollama run llama3.2:1b "What is a vector embedding? One sentence."
```
```
time ollama run llama3.2:3b "What is a vector embedding? One sentence."
```

![Comparing model sizes and speed](./images/ollama15.png?raw=true "Comparing model sizes and speed")

   The larger model takes roughly two to three times as long. Compare both the elapsed time and the quality of the answer - **that tradeoff is model selection.** There is no ranking here, only a choice. We default to 3B for this workshop because the answers are worth the wait; a batch job over ten thousand records might well choose 1B.

<br><br>

3. Every model in Ollama has a Modelfile behind it, even the ones you download. Let's look at the recipe that ships with Llama 3.2. Notice the `FROM` line pointing at a blob, the `TEMPLATE` block, and any baked-in `PARAMETER` values. We're about to write one of these ourselves.

```
ollama show --modelfile llama3.2:3b
```

![Viewing a model's Modelfile](./images/ollama16.png?raw=true "Viewing a model's Modelfile")

<br><br>

4. We've started a Modelfile for you, but left the interesting parts out. Open it either by clicking on [**modelfiles/Modelfile.shellcoach**](./modelfiles/Modelfile.shellcoach) or by entering the command below in the terminal.

```
code modelfiles/Modelfile.shellcoach
```

   There is a `FROM` line naming our base model, and then three `TODO` comments where the real instructions belong. As written, this would create a model that behaves exactly like the plain base model. **Note: this file is incomplete - we'll merge in the working version in the next step.**

![The skeleton Modelfile](./images/ollama17.png?raw=true "The skeleton Modelfile")

<br><br>

5. Now let's fill in the gaps. To keep things simple and avoid typing frustration, we already have the completed version in another file that we can merge into this one. Run the command below in the terminal.

```
code -d extra/Modelfile-shellcoach-complete.txt modelfiles/Modelfile.shellcoach
```

   Once you have run the command, you'll have a side-by-side view in your editor of the completed file and the *Modelfile.shellcoach* file. You can merge each section into *Modelfile.shellcoach* by hovering over the middle bar and clicking on the arrows pointing right. Go through each section, look at what it does, and then click to merge it in, one at a time. There are three sections - make sure to merge all the changes. When you are done, **save the file** with CTRL-S (CMD-S on a Mac).

![Merging the completed Modelfile](./images/ollama18.png?raw=true "Merging the completed Modelfile")

<br><br>

6. Read through what you just merged. Three things are happening:
   - **PARAMETER** lines set defaults that ship with the model - low `temperature` for consistency, a `num_ctx` of 4096, and a `num_predict` cap so answers can't ramble forever.
   - **SYSTEM** is the persona and the rules. It gets prepended to every single conversation, so users don't have to remember to ask for the format.
   - **MESSAGE** lines seed a fake exchange the model treats as prior conversation. This is few-shot priming - the cheapest way to lock in an output format.

   Note the `FROM llama3.2:3b` at the top. A Modelfile always names the base model explicitly - your customization is pinned to a specific model, which is exactly what makes it reproducible for a teammate.

<br><br>

7. Now build the model, then confirm it exists. This takes a few seconds - it isn't retraining anything, just layering our instructions on top of existing weights. Notice in the listing that `shellcoach` shows a size similar to the base model, because it shares the same underlying blobs rather than copying them.

```
ollama create shellcoach -f modelfiles/Modelfile.shellcoach
```
```
ollama list
```

![Creating a custom model](./images/ollama19.png?raw=true "Creating a custom model")

<br><br>

8. Ollama treats `shellcoach` as its own model, so it has to be loaded into memory separately the first time you use it. Warm it up now with the same program from Lab 1 - this time passing a model name.

```
python api/warmup.py shellcoach
```

   Notice how much faster this load is than the very first one in Lab 1. The underlying weight files are already in the operating system's disk cache, because `shellcoach` shares them with `llama3.2:3b`.

<br><br>

9. Let's try it. Notice you don't have to tell it how to answer - the format is already baked in.

```
ollama run shellcoach "How do I find files modified in the last 24 hours?"
```

![Running the custom model](./images/ollama20.png?raw=true "Running the custom model")

<br><br>

10. For contrast, ask the *base* model the exact same question. Compare the two answers - length, format, and whether the command came first.

```
ollama run llama3.2:3b "How do I find files modified in the last 24 hours?"
```

![Comparing custom model to base model](./images/ollama21.png?raw=true "Comparing custom model to base model")

<br><br>

11. Our model now has its own Modelfile, just like the downloaded ones did in step 3. Take a look - this is how you'd share a customization with a teammate. A Modelfile is a few lines of text you can put in version control; they run `ollama create` and get identical behavior.

```
ollama show --modelfile shellcoach
```

<br><br>

12. (Optional) Two things to try if you finish early. First, test the safety rule we wrote into the system prompt and look for the `CAUTION:` line. Then open the Modelfile, change `PARAMETER temperature 0.2` to `PARAMETER temperature 1.4`, save, rebuild, and rerun - re-running `ollama create` with the same name simply replaces the model. This edit-create-run loop is the fastest feedback cycle in the workshop.

```
ollama run shellcoach "How do I delete every .tmp file under my home directory?"
```
```
code modelfiles/Modelfile.shellcoach
```
```
ollama create shellcoach -f modelfiles/Modelfile.shellcoach
```
```
ollama run shellcoach "How do I check how much disk space is free?"
```

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 3 - Using Ollama from an application**

**Purpose: In this lab, we'll work through the three developer-facing ways into Ollama - the raw HTTP API with curl, the official Python library, and a framework - and see that all three hit the same endpoint. (approx. 12 minutes)**

1. Everything you've done so far went through a local HTTP service listening on port 11434. Confirm it's there with the first command - you should get back `Ollama is running`. The second gives you the same information as `ollama list`, but as JSON your code could consume. Then open the warmup program from Lab 1: `/api/tags` is where it gets its model list, and the whole warmup trick is a POST to `/api/generate` with a model and **no prompt**, which loads the weights and returns without generating anything.

```
curl http://localhost:11434
```
```
curl -s http://localhost:11434/api/tags | python3 -m json.tool
```
```
code api/warmup.py
```

![Listing models over the API](./images/ollama22.png?raw=true "Listing models over the API")

<br><br>

2. Now let's actually generate something. `/api/generate` is the single-turn endpoint - one prompt in, one completion out. `"stream": false` tells Ollama to send one complete JSON object when it's finished rather than a stream of fragments, and `num_predict` caps how long the answer can run.

```
curl -s http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "In two sentences, what is a REST API?",
  "stream": false,
  "options": { "temperature": 0.3, "num_predict": 60 }
}' | python3 -m json.tool
```

![Calling the generate endpoint](./images/ollama23.png?raw=true "Calling the generate endpoint")

   Look past the `response` field at the rest of that JSON. `eval_count` is how many tokens were generated, `eval_duration` is how long that took in nanoseconds, and `total_duration` covers the whole request. **These are how you measure a model on your own task instead of guessing from a leaderboard.**

<br><br>

3. Now the same request with streaming left on (it's the default). Instead of one object, you get a stream of newline-delimited JSON, one per token, with a final object where `done` is `true`. This is what makes a chat UI feel responsive - and on a CPU-only box it's the difference between usable and apparently broken.

```
curl -s http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "In two sentences, what is a REST API?",
  "options": { "num_predict": 60 }
}'
```

![Streaming responses](./images/ollama24.png?raw=true "Streaming responses")

<br><br>

4. `/api/generate` has no memory. For multi-turn conversation there's `/api/chat`, which takes a *messages* array. Notice we are sending the whole conversation - a system message, a user turn, the assistant's reply, and a new user turn that only makes sense in context. **Keep an eye on this shape; you'll see the exact same one twice more before the lab is over.**

```
curl -s http://localhost:11434/api/chat -d '{
  "model": "llama3.2:3b",
  "stream": false,
  "options": { "num_predict": 60 },
  "messages": [
    {"role": "system", "content": "You are terse and concrete."},
    {"role": "user", "content": "Name a good use for a local LLM."},
    {"role": "assistant", "content": "Summarizing internal documents that cannot leave your network."},
    {"role": "user", "content": "Why is that better than a hosted API?"}
  ]
}' | python3 -m json.tool
```

![Multi-turn chat over the API](./images/ollama25.png?raw=true "Multi-turn chat over the API")

<br><br>

5. That's the key mental model for the rest of the lab: **Ollama is stateless.** It did not remember anything between those calls - we resent the entire history. Any "memory" in an application is something your application is doing. We're about to write that code.

<br><br>

6. The official Python library is a thin, typed wrapper over those same endpoints, and it's already installed. We've provided a chat application with two pieces missing. Open it either by clicking on [**api/chat_app.py**](./api/chat_app.py) or with the command below.

```
code api/chat_app.py
```

   Read through it. There's a `MODEL` read from the environment, a `SYSTEM_PROMPT`, an `ask()` function that is supposed to call the model, and a `main()` loop that collects input. Find the two `TODO` markers. **Note: this file is incomplete - it will raise a `NotImplementedError` if you run it now.**

![The skeleton chat application](./images/ollama26.png?raw=true "The skeleton chat application")

<br><br>

7. As before, we'll use the "view differences and merge" technique to learn about the code we'll be working with. Run the command below in the terminal.

```
code -d extra/chat_app-complete.txt api/chat_app.py
```

   You'll get a side-by-side view of the completed code and the *chat_app.py* file. Merge each section into *chat_app.py* by hovering over the middle bar and clicking on the arrows pointing right. Take a moment to look at each section as you merge it in. There are three sections - make sure to merge all the changes. When you're done, **save the file** with CTRL-S (CMD-S on a Mac).

![Merging the completed chat application](./images/ollama27.png?raw=true "Merging the completed chat application")

<br><br>

8. Look at what you merged into `ask()`:
   - `ollama.chat(...)` takes the same `model`, `messages`, and `options` you sent as raw JSON in step 4. The library is not doing anything you couldn't do with curl - it is saving you the typing and giving you types.
   - `stream=True` turns the return value into an iterator - we print each chunk as it arrives instead of waiting for the whole answer. That is step 3's newline-delimited JSON, handled for you.
   - We accumulate the pieces into `reply` so we have the complete text to store in our history.

   And the second block: `messages.append({"role": "assistant", ...})`. **That one line is the entire "memory" of this application.**

<br><br>

9. Now run it. At the `You:` prompt, ask the first question below, wait for the answer, then ask the follow-up - which has no meaning on its own. Watch the `[history: N messages]` counter grow after each turn; that's the conversation being resent in full every time. Exit with CTRL-C when you've seen it.

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

10. Let's prove the memory claim. Open the file, comment out the `messages.append({"role": "assistant", ...})` line by putting a `#` in front of it, and save. Run it again, ask the same first question, then ask the follow-up - this time it should land with no context at all, because the model has no idea what "that" refers to. Exit with CTRL-C, then **remove the `#` and save** so the file is correct if you come back to it.

```
code api/chat_app.py
```
```
python api/chat_app.py
```

![The conversation loses its memory](./images/ollama29.png?raw=true "The conversation loses its memory")

<br><br>

11. Finally, the layer most developers actually reach for: a framework. LangChain has a native Ollama integration, and `langchain-ollama` is already installed. Open the example and run it.

```
code api/simple_langchain.py
```
```
python api/simple_langchain.py "What is the capital of France?"
```

![Ollama through LangChain](./images/ollama30.png?raw=true "Ollama through LangChain")

   Three things to notice, and they are the point of this whole lab:
   - `ChatOllama(model=..., temperature=..., num_predict=...)` sets **the same options** you typed into the `options` block in steps 2 - 4.
   - The message list - `system`, `human`, `ai`, `human` - is **the same shape** you sent to `/api/chat` by hand in step 4.
   - Underneath, LangChain is calling **the same endpoint** on the same local service. It did not add memory; the script still passes the whole conversation.

   A framework buys you one interface across many model providers - swap `ChatOllama` for a hosted provider's class and the rest of your chain is unchanged. It costs you a dependency and a layer of indirection to debug through. Now you know exactly what is underneath it.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 4 - Cloud models and wiring Ollama into your tools**

**Purpose: In this lab, we'll run a model far too large for this machine using the same commands and the same code, then use `ollama launch` to point a real coding tool at Ollama without editing a single config file. (approx. 9 minutes)**

**Note: this lab needs a free ollama.com account. If you ran the optional signin step at the end of Lab 1, you are already set. If not, step 1 handles it.**

1. Ollama Cloud runs large models on Ollama's hardware and exposes them through the exact API you have been using all workshop. The free tier is enough for this lab. If you already signed in during the break, this will tell you so; otherwise it prints a URL - open it, create a free account, and come back.

```
ollama signin
```

![Signed in to ollama.com](./images/ollama31.png?raw=true "Signed in to ollama.com")

<br><br>

2. Cloud models carry a `-cloud` tag. Pulling one downloads no weights at all - it just registers the model locally so your machine knows where to route requests. Notice how fast this is compared to the multi-gigabyte pulls at setup time.

   **Cloud model names change frequently. If the name below is gone, open https://ollama.com/search?c=cloud and substitute any model whose tag ends in `-cloud`.**

```
ollama pull gpt-oss:120b-cloud
```

<br><br>

3. Confirm what just landed. Compare the `SIZE` column for the cloud model against `llama3.2:3b` - there are no weights on your disk.

```
ollama list
```

![A cloud model in the local list](./images/ollama32.png?raw=true "A cloud model in the local list")

<br><br>

4. Now run it. This is a 120-billion-parameter model - roughly forty times the size of the one you have been using, and impossible to fit in this codespace. **The command is identical to every other `ollama run` you have typed today.**

```
ollama run gpt-oss:120b-cloud "Compare a 3B local model with a 120B hosted model for a code review assistant. Be specific about where each one wins."
```

![Running a cloud-hosted model](./images/ollama33.png?raw=true "Running a cloud-hosted model")

<br><br>

5. Two things to notice about that answer: it arrived faster than your local 3B model despite being forty times larger (someone else's GPUs are doing the work), and it is visibly better reasoned. That is the trade you are making - speed and quality in exchange for your prompt leaving the machine.

<br><br>

6. Check what this cost you locally. The cloud model does not appear as loaded, because nothing is loaded - your machine only forwarded the request.

```
ollama ps
```

<br><br>

7. Now the important part: **your code does not change either.** The chat application you finished in Lab 3 reads its model from an environment variable, so point it at the cloud model and run it. Ask it anything, then exit with CTRL-C.

```
OLLAMA_MODEL=gpt-oss:120b-cloud python api/chat_app.py
```

![The same app against a cloud model](./images/ollama34.png?raw=true "The same app against a cloud model")

   Same library, same `ollama.chat()` call, same streaming loop, same message history. Only the model name is different. This is the single strongest argument for building against Ollama's API rather than a vendor SDK - local and hosted are one line apart.

<br><br>

8. Let's finish somewhere useful. `ollama launch` configures and starts real developer tools against your Ollama models, without you writing any environment variables or config files. See what it supports.

```
ollama launch --help
```

![The launch command](./images/ollama35.png?raw=true "The launch command")

   You should see integrations for coding tools such as **Claude Code, OpenCode, Codex, VS Code, and Droid**. (This command needs Ollama 0.15 or later - check with `ollama --version` if you don't see it.)

<br><br>

9. Run it in configure-only mode. The `--config` flag writes the integration's settings and stops, instead of trying to start the tool - which is what we want here, since these tools are not installed in the codespace. Follow the prompts and pick the cloud model you pulled when it asks.

```
ollama launch vscode --config --model gpt-oss:120b-cloud
```

   **Note:** this is an interactive command. If a tool is not installed, it will tell you so - that is a normal outcome here and not a lab failure. The point is to see that wiring a real editor or agent to a local or cloud model is one command rather than an afternoon of environment variables.

<br><br>

10. (Optional) Try it against a different integration and a local model, to see that the same command covers both worlds.

```
ollama launch codex --config --model llama3.2:3b
```

<br><br>

11. **On staying free:** the free tier covers light usage, one cloud model at a time, with limits that reset on a rolling window. Everything else in this workshop runs locally at zero cost forever. Check your usage any time at https://ollama.com/settings. If you would rather not stay signed in, sign out now.

```
ollama signout
```

<p align="center">
**[END OF LAB]**
</p>
</br></br>

<br>

<p align="center">
<b>PART TWO - TAKE-HOME LABS</b>
</p>

<p align="center">
<i>These go deeper on material the slides cover. Nothing here is required for the in-class session.</i>
</p>

<br>

**Lab 5 - Managing models on disk and in memory**

**Purpose: In this lab, we'll work through the model management commands and see how Ollama shares storage between models. (approx. 10 minutes)**

1. Start with what's on disk and what's loaded. The size in `ollama ps` is *larger* than the size in `ollama list` - disk size is the weights, while loaded size adds memory for the context window.

```
ollama list
```
```
ollama ps
```

<br><br>

2. There are focused versions of the `show` flag. Try these and see what each one gives you on its own.

```
ollama show --parameters llama3.2:3b
```
```
ollama show --template llama3.2:3b
```
```
ollama show --system shellcoach
```

<br><br>

3. On a 4-core codespace, memory is worth managing. You can unload a model immediately instead of waiting for its timer to expire. Load one, unload it, and confirm.

```
ollama run llama3.2:1b "Say hello."
```
```
ollama ps
```
```
ollama stop llama3.2:1b
```
```
ollama ps
```

<br><br>

4. Models can be copied under a new name. This is cheap - it does not duplicate the underlying weights, it just adds a new tag pointing at the same blobs. Watch the total in `ollama list` and notice it barely moves.

```
ollama cp llama3.2:1b my-experiment
```
```
ollama list
```

<br><br>

5. And removed. `ollama rm` deletes the *tag*; disk space is reclaimed only when no tag references those blobs any more.

```
ollama rm my-experiment
```

<br><br>

6. `keep_alive` controls how long a model lingers after its last request - the default is 5 minutes. You can set it per request. The call below loads the model and pins it in memory indefinitely (`-1`); a value of `0` would unload it the moment the request finishes. Run it, then check the *UNTIL* column.

```
curl -s http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "keep_alive": -1
}' | python3 -m json.tool
```
```
ollama ps
```

<br><br>

7. Put it back to a normal policy so it doesn't hold memory forever.

```
curl -s http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "keep_alive": "5m"
}' | python3 -m json.tool
```

<br><br>

8. For a whole server, the same policy is set with the `OLLAMA_KEEP_ALIVE` environment variable before starting `ollama serve`. That is the most common production tuning knob, along with `OLLAMA_CONTEXT_LENGTH` and `OLLAMA_MAX_LOADED_MODELS`.

<br><br>

9. Finally, let's look at where the real models come from. Open a new browser tab and go to https://ollama.com/search. Use the filter controls to browse by capability - `tools`, `vision`, `embedding`, `thinking`. Pick a model, look at its card, and find its available tag sizes.

![Browsing the model library](./images/ollama36.png?raw=true "Browsing the model library")

   When you're picking a model for real work, the practical checklist is:
   - Does it fit in your available RAM? (roughly: file size + 1 - 2 GB of overhead)
   - Does it have the capability you need - tool calling, vision, embeddings?
   - Is the context window big enough for your prompts?
   - Is the license acceptable for what you're building?

<br><br>

10. (Optional) Pull one more small model and compare its `ollama show` output to Llama 3.2. Check `ollama list` before and after so you know what you're adding to a 32 GB codespace.

```
ollama pull qwen3:0.6b
```
```
ollama show qwen3:0.6b
```

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 6 - The REST API in depth**

**Purpose: In this lab, we'll call the API from a program instead of curl, and use structured output to get JSON you can rely on. (approx. 10 minutes)**

1. We've provided a script that calls `/api/tags` and `/api/generate` both ways using nothing but the `requests` library - no Ollama client involved. Open it and look at how little there is to it.

```
code api/rest_generate.py
```

<br><br>

2. Run it. It will list your models, do one non-streaming call, then repeat the same prompt with streaming so you can watch the difference. Notice the timing line printed after the non-streaming call - that comes straight from `eval_count` and the duration fields.

```
python api/rest_generate.py
```

![Running the REST client script](./images/ollama37.png?raw=true "Running the REST client script")

<br><br>

3. You can pass your own prompt as arguments.

```
python api/rest_generate.py Explain what a Modelfile is in one sentence.
```

<br><br>

4. Now the most practically useful API feature: structured output. Instead of parsing prose with regexes, you hand Ollama a JSON Schema in the `format` field and the reply is constrained to match it. Open the script and look at the `SCHEMA` object.

```
code api/structured_output.py
```

<br><br>

5. Run it. The raw response prints first, then the same thing after `json.loads()` - which is guaranteed to succeed because of the schema.

```
python api/structured_output.py PostgreSQL
```

![Structured JSON output](./images/ollama38.png?raw=true "Structured JSON output")

<br><br>

6. Try it with something else and notice that the *shape* of the result stays identical even though the content changes. That is the whole point.

```
python api/structured_output.py Kubernetes
```

<br><br>

7. **Important caveat:** the schema guarantees the shape, not the truth. A well-formed object can still be populated with wrong facts. Run the command below on something obscure and check whether `first_released` is actually right. Validate semantics separately in real code.

```
python api/structured_output.py Erlang
```

<br><br>

8. (Optional) Open `api/structured_output.py` and add a new property to `SCHEMA` - for example `"maintained_by": {"type": "string"}` - then rerun and see the model fill it in.

```
code api/structured_output.py
```
```
python api/structured_output.py PostgreSQL
```

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 7 - The troubleshooting toolkit and OpenAI compatibility**

**Purpose: In this lab, we'll reuse existing OpenAI code against Ollama, reach the cloud with an API key instead of a signin, and work through the handful of commands worth knowing when something breaks. (approx. 8 minutes)**

1. Ollama serves an OpenAI-compatible surface at `/v1`. That means most code already written against OpenAI works by changing two things: the base URL and the model name. Confirm the endpoint is there.

```
curl -s http://localhost:11434/v1/models | python3 -m json.tool
```

![The OpenAI-compatible model list](./images/ollama39.png?raw=true "The OpenAI-compatible model list")

<br><br>

2. We've provided a script that uses the *official OpenAI Python SDK* - not the Ollama library - pointed at your local server. Open it and look at how ordinary it is. The `api_key` is required by the SDK but ignored by Ollama, so any string works.

```
code api/openai_compat.py
```

<br><br>

3. Run it. Nothing left this codespace, but the code is indistinguishable from code that would call a hosted provider. Swapping `base_url` to a real vendor is a one-line change.

```
python api/openai_compat.py
```

![OpenAI SDK against local Ollama](./images/ollama40.png?raw=true "OpenAI SDK against local Ollama")

<br><br>

4. In Lab 4 you reached Ollama Cloud by signing in, which routes cloud requests through your local server. There is a second way: talk to `https://ollama.com` directly with an API key, which is what you'd do from a server or a CI job where there is no interactive signin. Create a key at https://ollama.com/settings/keys, then export it.

```
export OLLAMA_API_KEY=your_key_here
```

<br><br>

5. Run the provided script. Read the source first - notice that the `client.chat()` call is character-for-character the same as the one in `chat_app.py`. Only the client construction changed.

```
code api/cloud_chat.py
```
```
python api/cloud_chat.py
```

<br><br>

6. Now the troubleshooting toolkit. First, is the service even up?

```
curl -s http://localhost:11434/api/tags > /dev/null && echo "Ollama is up" || echo "Ollama is NOT running"
```

<br><br>

7. If it isn't, the server log will usually say why.

```
tail -30 /tmp/ollama.log
```

<br><br>

8. If you ever get `address already in use` on port 11434, there's a stale server. Stop everything, then start it cleanly. Note that `startOllama.sh` also kicks off the warmup from Lab 1 in the background, so your models come back ready.

```
bash scripts/shutdown_ollama.sh
```
```
bash scripts/startOllama.sh
```

<br><br>

9. If a model has been idle long enough to unload, you don't have to wait for the next prompt to reload it. Warm it deliberately, and pin it for as long as you need.

```
python api/warmup.py llama3.2:3b 1h
```
```
ollama ps
```

<br><br>

10. And if you're running low on disk, remove models you're done with. Run `ollama list` first and pick something you no longer need - for example the `shellcoach` model from Lab 2, `my-experiment` if it survived Lab 5, or `qwen3:0.6b` if you pulled it.

```
ollama list
```
```
ollama rm shellcoach
```

<br><br>

11. **Where to go next:**
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
