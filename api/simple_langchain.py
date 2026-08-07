# simple_langchain.py - The same local model, reached through LangChain.
# Lab 3 - Introduction to Ollama
#
# This is the fourth and last way into Ollama that we cover:
#
#   1. The CLI            ollama run                  (Lab 1)
#   2. The raw REST API   curl .../api/chat           (Lab 3, steps 2 - 4)
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
    print(f"\n--- invoke() with {MODEL} ---")
    response = llm.invoke(prompt)
    print(response.content.strip())


def multi_turn():
    """A messages list - the same shape you sent to /api/chat by hand."""
    print(f"\n--- invoke() with a message list ---")
    messages = [
        ("system", "You are terse and concrete. Two sentences maximum."),
        ("human", "Name one good use for a local LLM."),
        ("ai", "Summarizing internal documents that cannot leave your network."),
        ("human", "Why is that better than a hosted API?"),
    ]
    response = llm.invoke(messages)
    print(response.content.strip())
    print("\nSame roles, same history-you-resend rule. LangChain did not add memory -")
    print("we still passed the whole conversation. Ollama is still stateless.")


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
