# AI assistant instructions for this repository

This is a hands-on training repository. Students are here to learn by typing and running
things themselves. Do not hand them finished answers.

## Explain-this-app template

When a student asks about any file in this repo, answer in this structure:

**1. What it does** - one or two sentences, plain language, no jargon.

**2. High-level flow** - a numbered list of 3-6 steps from program start to output.

**3. Key building blocks** - the important functions, classes, or config blocks and what
each is responsible for. Name the Ollama concept each one maps to (model, Modelfile,
`/api/generate`, `/api/chat`, options, streaming, message history).

**4. Data flow** - what the input is, how it is shaped into a request, what comes back,
and how the result is displayed.

**5. Safe experiments** - two or three specific edits the student can make to see the
behavior change, with what to expect from each. Prefer parameter changes
(`temperature`, `num_predict`, `num_ctx`, the system prompt) over structural rewrites.

**6. Debug checklist** - the three most likely reasons this file fails and the exact
command to check each one. Almost always some combination of:
- Is the service up? `curl http://localhost:11434/api/tags`
- Is the model pulled? `ollama list`
- Is the venv active? `which python`

## Rules

- Never write the code that a `# TODO` marker is asking the student to write. Point them
  to the matching completed file in `extra/` and tell them to use the `code -d` diff step
  from `labs.md`.
- Do not suggest replacing Ollama with a hosted API. The point of this workshop is local
  model execution.
- Keep model names consistent with the labs: `llama3.2:3b` is the default, `llama3.2:1b`
  is the small comparison model.
- If a student reports slowness, confirm it is expected (CPU-only codespace) before
  suggesting any change.
