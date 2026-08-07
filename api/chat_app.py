# chat_app.py - A small multi-turn chat application on the Ollama Python library.
# Lab 5 - Introduction to Ollama
#
# Two things to notice:
#   1. The library is a thin wrapper over the same REST API from Lab 4.
#   2. Ollama does NOT remember your conversation. WE keep the history and
#      resend it every turn. That is what makes this feel like a chat.
#
# NOTE: this file is incomplete on purpose. It will not work until you merge in
# the finished code in the next lab step.

import os
import sys

import ollama

MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")

SYSTEM_PROMPT = (
    "You are a concise technical assistant. "
    "Answer in three sentences or fewer unless the user asks for more detail."
)


def ask(messages):
    """Send the whole conversation to Ollama and stream the reply to the screen."""
    # TODO 1: Call ollama.chat() with model=MODEL, messages=messages, stream=True
    #         and options for temperature and num_predict. Loop over the chunks,
    #         print each piece as it arrives, and build up the full reply string.
    raise NotImplementedError("TODO 1: call ollama.chat() and stream the reply")


def main():
    print(f"Chatting with {MODEL}. Press Ctrl+C to quit.")
    print("Try a follow-up question like 'why?' to prove it remembers.\n")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        print("Model: ", end="", flush=True)
        answer = ask(messages)

        # TODO 2: Append the model's own answer to 'messages' so the next turn
        #         has the full context. Without this, every turn starts over.

        print(f"[history: {len(messages)} messages]\n")


if __name__ == "__main__":
    try:
        main()
    except ollama.ResponseError as e:
        print(f"\nOllama returned an error: {e.error}")
        print(f"Is '{MODEL}' pulled? Check with: ollama list")
        sys.exit(1)
    except ConnectionError:
        print("\nCould not reach Ollama. Try: bash scripts/startOllama.sh")
        sys.exit(1)
