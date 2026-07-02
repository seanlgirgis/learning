"""Same flow as 03_build_index_query.py — but LLM + embeddings come from config.py."""

import os
from pathlib import Path

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

import config

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "company_knowledge"


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Run set_env.ps1 first — OPENAI_API_KEY missing.")

    Settings.llm = OpenAI(model=config.OPENAI_MODEL, temperature=config.LLM_TEMPERATURE)
    Settings.embed_model = OpenAIEmbedding(model=config.OPENAI_EMBEDDING_MODEL)

    print("Using LLM:", config.OPENAI_MODEL)
    print("Using embeddings:", config.OPENAI_EMBEDDING_MODEL)
    print()

    documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    questions = [
        "What is the support escalation rule for Sev-1 incidents?",
        "Which product is better for dashboard-style reports?",
        "What changed after the May 2026 analytics outage?",
        "Can I upload API keys into an AI tool?",
        "Who is the CEO of Northwind Analytics?",
    ]

    for question in questions:
        print("=" * 80)
        print(f"QUESTION: {question}")
        response = query_engine.query(question)
        print()
        print("ANSWER:")
        print(response)
        print()


if __name__ == "__main__":
    main()