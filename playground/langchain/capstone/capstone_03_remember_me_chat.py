"""Capstone 03 — Remember-Me Chat: buffer memory + REPL.

Guide: capstone/capstone03.md
Lab mirror: playground/langchain/33.memory.py

Run:
    cd D:\\Workarea\\learning\\playground\\langchain\\capstone
    python capstone_03_remember_me_chat.py
    python capstone_03_remember_me_chat.py --demo cat
    python capstone_03_remember_me_chat.py --demo alice
    python capstone_03_remember_me_chat.py --memory summary
    python capstone_03_remember_me_chat.py --save data/chat_memory.json
    python capstone_03_remember_me_chat.py --load data/chat_memory.json
    python capstone_03_remember_me_chat.py -q "What is my name?" --load data/chat_memory.json

Needs: set_env.ps1 + network (Watsonx LLM).
"""

from __future__ import annotations

import warnings

# Capstone demo: LangChain classic memory/chain APIs are deprecated but still used in Lab 33.
warnings.simplefilter("ignore", DeprecationWarning)
warnings.showwarning = lambda *args, **kwargs: None

import argparse
import json
import sys
from pathlib import Path

# watson_llm lives in playground/langchain/ (parent of capstone/)
_CAPSTONE_DIR = Path(__file__).resolve().parent
_LANGCHAIN_ROOT = _CAPSTONE_DIR.parent
if str(_LANGCHAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(_LANGCHAIN_ROOT))
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_classic.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from watson_llm import make_watsonx_llm

DEFAULT_MEMORY_PATH = _CAPSTONE_DIR / "data" / "chat_memory.json"
MEMORY_VERSION = 1

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


def make_chat_llm():
    return make_watsonx_llm(CHAT_LLM_PARAMS)


def build_memory(
    memory_type: str,
    *,
    chat_memory: ChatMessageHistory | None = None,
):
    llm = make_chat_llm()
    if memory_type == "summary":
        if chat_memory is not None:
            return ConversationSummaryMemory(llm=llm, chat_memory=chat_memory)
        return ConversationSummaryMemory(llm=llm)
    if chat_memory is not None:
        return ConversationBufferMemory(chat_memory=chat_memory)
    return ConversationBufferMemory()


def build_conversation_chain(
    *,
    memory_type: str = "buffer",
    chat_memory: ChatMessageHistory | None = None,
) -> ConversationChain:
    return ConversationChain(
        llm=make_chat_llm(),
        memory=build_memory(memory_type, chat_memory=chat_memory),
        prompt=CAPSTONE_PROMPT,
        verbose=False,
    )


def chat_once(chain: ConversationChain, user_input: str) -> str:
    result = chain.invoke(input=user_input)
    return str(result.get("response", result)).strip()


def message_role(message: BaseMessage) -> str:
    if isinstance(message, HumanMessage):
        return "human"
    if isinstance(message, AIMessage):
        return "ai"
    return message.type


def message_from_role(role: str, content: str) -> BaseMessage:
    if role == "human":
        return HumanMessage(content=content)
    return AIMessage(content=content)


def messages_to_serializable(messages: list[BaseMessage]) -> list[dict[str, str]]:
    return [{"role": message_role(m), "content": m.content} for m in messages]


def history_from_serializable(rows: list[dict[str, str]]) -> ChatMessageHistory:
    history = ChatMessageHistory()
    for row in rows:
        history.add_message(message_from_role(row["role"], row["content"]))
    return history


def get_chat_messages(chain: ConversationChain) -> list[BaseMessage]:
    chat_memory = getattr(chain.memory, "chat_memory", None)
    if chat_memory is None:
        return []
    return list(chat_memory.messages)


def memory_type_of(chain: ConversationChain) -> str:
    if isinstance(chain.memory, ConversationSummaryMemory):
        return "summary"
    return "buffer"


def replay_summary_from_messages(chain: ConversationChain, rows: list[dict[str, str]]) -> None:
    """Rebuild summary state by replaying human/ai pairs (load path)."""
    if not isinstance(chain.memory, ConversationSummaryMemory):
        return
    pending_human: str | None = None
    for row in rows:
        if row["role"] == "human":
            pending_human = row["content"]
        elif row["role"] == "ai" and pending_human is not None:
            chain.memory.save_context({"input": pending_human}, {"output": row["content"]})
            pending_human = None


def save_memory(chain: ConversationChain, path: Path) -> None:
    rows = messages_to_serializable(get_chat_messages(chain))
    payload = {
        "version": MEMORY_VERSION,
        "memory_type": memory_type_of(chain),
        "messages": rows,
        "summary": chain.memory.buffer if memory_type_of(chain) == "summary" else None,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
    print(f"Saved memory → {path} ({len(rows)} messages)")


def load_memory_payload(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def build_chain_from_saved(path: Path, *, memory_type: str) -> ConversationChain:
    payload = load_memory_payload(path)
    saved_type = payload.get("memory_type", "buffer")
    if saved_type != memory_type:
        print(f"Note: file memory_type={saved_type!r}, CLI --memory={memory_type!r}")
        memory_type = saved_type
    rows = payload.get("messages", [])
    history = history_from_serializable(rows) if rows else None
    chain = build_conversation_chain(memory_type=memory_type, chat_memory=history)
    if memory_type == "summary" and rows:
        replay_summary_from_messages(chain, rows)
    print(f"Loaded memory ← {path} ({len(rows)} messages, type={memory_type})")
    return chain


def peek_memory(chain: ConversationChain) -> None:
    print(f"\n--- Memory ({memory_type_of(chain)}) ---")
    print(chain.memory.buffer)
    print(f"Buffer size (chars): {len(chain.memory.buffer)}")


def run_scripted_turns(chain: ConversationChain, inputs: list[str], *, title: str) -> None:
    print(f"\n=== {title} ===")
    for i, user_input in enumerate(inputs, start=1):
        print(f"\n--- Turn {i} ---")
        print(f"You: {user_input}")
        reply = chat_once(chain, user_input)
        print(f"AI: {reply}")
    print(f"\n=== End: {title} ===")


def run_repl(chain: ConversationChain) -> None:
    print("Remember-Me Chat (empty line or 'quit' to exit)")
    while True:
        user_input = input("You: ").strip()
        if not user_input or user_input.lower() in ("quit", "exit"):
            break
        print(f"AI: {chat_once(chain, user_input)}")
        print()


def run_one_shot(chain: ConversationChain, question: str) -> None:
    print(f"You: {question}")
    print(f"AI: {chat_once(chain, question)}")


def demo_little_cat(chain: ConversationChain) -> None:
    run_scripted_turns(
        chain,
        [
            "Hello, I am a little cat. Who are you?",
            "What can you do?",
            "Who am I?",
        ],
        title="Little cat demo",
    )


def demo_alice(*, memory_type: str = "buffer") -> ConversationChain:
    alice_history = ChatMessageHistory()
    alice_history.add_user_message("Hello, my name is Alice.")
    alice_history.add_ai_message(
        "Hello Alice! It's nice to meet you. How can I help you today?"
    )
    chain = build_conversation_chain(memory_type=memory_type, chat_memory=alice_history)
    run_scripted_turns(
        chain,
        [
            "My favorite color is blue.",
            "I enjoy hiking in the mountains.",
            "What activities would you recommend for me?",
            "What was my favorite color again?",
            "Can you remember both my name and my favorite color?",
        ],
        title="Alice demo",
    )
    return chain


def finish_session(chain: ConversationChain, *, peek: bool, save: Path | None) -> None:
    if peek:
        peek_memory(chain)
    if save is not None:
        save_memory(chain, save)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Capstone 03 — Remember-Me Chat with buffer or summary memory.",
    )
    parser.add_argument(
        "--memory",
        choices=["buffer", "summary"],
        default="buffer",
        help="buffer = full transcript; summary = LLM-compressed history (stretch)",
    )
    parser.add_argument(
        "--load",
        type=Path,
        metavar="PATH",
        help="Load session from JSON (from a prior --save)",
    )
    parser.add_argument(
        "--save",
        type=Path,
        nargs="?",
        const=DEFAULT_MEMORY_PATH,
        metavar="PATH",
        help="Save session on exit (default: data/chat_memory.json if PATH omitted)",
    )
    parser.add_argument(
        "--peek",
        action="store_true",
        help="Print memory buffer when the session ends",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--demo",
        choices=["cat", "alice"],
        help="Run scripted Lab 33 demo instead of REPL",
    )
    mode.add_argument(
        "-q",
        "--question",
        metavar="TEXT",
        help="One-shot question then exit (use with --load for recall)",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.load:
        chain = build_chain_from_saved(args.load, memory_type=args.memory)
    else:
        chain = build_conversation_chain(memory_type=args.memory)
        if args.memory == "summary":
            print(
                "Summary memory: empty session — tell me your name first, "
                "or use --load data/chat_memory.json"
            )

    if args.demo == "cat":
        demo_little_cat(chain)
        finish_session(chain, peek=args.peek or True, save=args.save)
        return

    if args.demo == "alice":
        chain = demo_alice(memory_type=args.memory)
        finish_session(chain, peek=args.peek or True, save=args.save)
        return

    if args.question:
        run_one_shot(chain, args.question)
        finish_session(chain, peek=args.peek, save=args.save)
        return

    run_repl(chain)
    finish_session(chain, peek=args.peek, save=args.save)


if __name__ == "__main__":
    main()