"""Capstone 03 — barebones remember-me chat (buffer memory + REPL only).

Stripped: CLI, save/load, demos, summary memory.
Full version: capstone_03_remember_me_chat.py

Run:
    cd D:\\Workarea\\learning\\playground\\langchain\\capstone
    python capstone_03_remember_me_chat_bare.py
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

warnings.simplefilter("ignore", DeprecationWarning)
warnings.showwarning = lambda *args, **kwargs: None

_LANGCHAIN_ROOT = Path(__file__).resolve().parent.parent
if str(_LANGCHAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(_LANGCHAIN_ROOT))

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.prompts import PromptTemplate
from watson_llm import make_watsonx_llm

CHAT_LLM_PARAMS = {
    GenParams.TEMPERATURE: 0.2,
    GenParams.MAX_NEW_TOKENS: 256,
}

CAPSTONE_PROMPT = PromptTemplate(
    input_variables=["history", "input"],
    template="""You are a helpful assistant in a multi-turn chat.

Rules:
- Reply with ONE short assistant message only.
- Do NOT write "Human:" or pretend the user said something else.
- Do NOT continue the conversation for the user.
- Remember facts the user stated earlier in this chat.

Current conversation:
{history}

Human: {input}
AI:""",
)


def build_chain() -> ConversationChain:
    return ConversationChain(
        llm=make_watsonx_llm(CHAT_LLM_PARAMS),
        memory=ConversationBufferMemory(),
        prompt=CAPSTONE_PROMPT,
        verbose=False,
    )


def chat_once(chain: ConversationChain, user_input: str) -> str:
    result = chain.invoke(input=user_input)
    return str(result.get("response", result)).strip()


def main() -> None:
    chain = build_chain()
    print("Remember-Me Chat (empty line or 'quit' to exit)")
    while True:
        user_input = input("You: ").strip()
        if not user_input or user_input.lower() in ("quit", "exit"):
            break
        print(f"AI: {chat_once(chain, user_input)}")
        print()


if __name__ == "__main__":
    main()