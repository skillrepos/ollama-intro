# simple_langchain.py - The same local model, reached through LangChain.
# Lab 3 - Introduction to Ollama
#
# This is the fourth and last way into Ollama that we cover:
#
#   1. The CLI            ollama run                  (Lab 1)
#   2. The raw REST API   curl .../api/chat           (Lab 3, steps 3 - 5)
#   3. The Ollama library ollama.chat()               (chat_app.py)
#   4. A framework        ChatOllama().invoke()       (this file)
#
# Every layer is talking to the same local service on port 11434. A framework
# buys you a common interface across model providers - swap ChatOllama for a
# hosted provider's class and the rest of your chain is unchanged. It costs you
# a dependency and a layer of indirection you have to debug through.

import os
import sys

from langchain_ollama import ChatOllama

MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")

# The same knobs you set with /set parameter, in a Modelfile, and in the
# "options" block of a raw API call - just spelled as constructor arguments.
llm = ChatOllama(
    model=MODEL,
    temperature=0.3,
    num_predict=80,
)


def single_turn(prompt):
    """One prompt in, one answer out - the LangChain equivalent of /api/generate."""
    print(f"\n--- invoke() with a single string (the /api/generate shape) ---")
    print(f"    prompt: {prompt}")
    response = llm.invoke(prompt)
    print(response.content.strip())


def multi_turn():
    """A messages list - the same conversation you sent to /api/chat in step 5."""
    print("\n--- invoke() with a conversation (the /api/chat shape) ---")
    messages = [
        ("system", "You are terse and concrete."),
        ("human", "My server has 6 GB of RAM and no GPU."),
        ("ai", "Noted - 6 GB, CPU only."),
        ("human", "How much RAM does my server have?"),
    ]
    for role, text in messages:
        print(f"    {role:<7} {text}")
    response = llm.invoke(messages)
    print(f"    reply   {response.content.strip()}")
    print("\nThat is step 5's curl call, run through a framework instead:")
    print("  LangChain system / human / ai  ==  API system / user / assistant")
    print("Same roles, same array, same service on port 11434. LangChain added no")
    print("memory - we still passed the whole conversation. Ollama is still stateless.")


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or input("Enter your prompt: ").strip()
    if not prompt:
        prompt = "What is the capital of France?"

    try:
        single_turn(prompt)
        multi_turn()
    except Exception as e:
        print(f"\nRequest failed: {e}")
        print("Is Ollama running? Try: bash scripts/startOllama.sh")
        print(f"Is '{MODEL}' pulled?  Check with: ollama list")
        sys.exit(1)
