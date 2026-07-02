"""Module 3 — Lab 3: icebreaker bot REPL (05.pdf, mock LinkedIn).

Proxycurl is dead — we load data/mock_linkedin_profile.json instead.

Run from lab/module3 (needs set_env.ps1):
  python lab_03_icebreaker.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from llama_index.core import Document, PromptTemplate, Settings, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

import config

ROOT = Path(__file__).resolve().parent
PROFILE_PATH = ROOT / "data" / "mock_linkedin_profile.json"


def load_mock_profile() -> dict:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def build_index(profile: dict) -> VectorStoreIndex:
    doc = Document(text=json.dumps(profile), metadata={"source": "mock_linkedin"})
    nodes = SentenceSplitter(chunk_size=config.CHUNK_SIZE).get_nodes_from_documents([doc])
    return VectorStoreIndex(nodes, show_progress=True)


def generate_initial_facts(index: VectorStoreIndex) -> str:
    engine = index.as_query_engine(
        similarity_top_k=config.SIMILARITY_TOP_K,
        text_qa_template=PromptTemplate(config.INITIAL_FACTS_TEMPLATE),
    )
    return str(
        engine.query("Provide three interesting facts about this person's career or education.")
    )


def answer_question(index: VectorStoreIndex, question: str) -> str:
    engine = index.as_query_engine(
        similarity_top_k=config.SIMILARITY_TOP_K,
        text_qa_template=PromptTemplate(config.USER_QUESTION_TEMPLATE),
    )
    return str(engine.query(question))


def chat_loop(index: VectorStoreIndex) -> None:
    print("\nAsk about the profile. Type exit / quit / bye to stop.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "bye"}:
            print("Bot: Goodbye!")
            break
        print(f"Bot: {answer_question(index, user_input)}\n")


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Run set_env.ps1 first — OPENAI_API_KEY missing.")

    Settings.llm = OpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.0)
    Settings.embed_model = OpenAIEmbedding(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )

    profile = load_mock_profile()
    print(f"Loaded mock profile: {profile['full_name']}")

    index = build_index(profile)
    print("\n--- 3 icebreaker facts ---")
    print(generate_initial_facts(index))
    chat_loop(index)


if __name__ == "__main__":
    main()