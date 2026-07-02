"""Module 3 — Lab 2: embed, index, retrieve, answer (02.md).

Run from lab/module3 (needs set_env.ps1):
  python lab_02_index_query.py
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


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Run set_env.ps1 first — OPENAI_API_KEY missing.")

    # Course uses watsonx here; locally we point Settings at OpenAI.
    Settings.llm = OpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.0)
    Settings.embed_model = OpenAIEmbedding(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )

    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    print(f"Profile: {profile['full_name']} — {profile['headline']}\n")

    # --- Split profile JSON into nodes ---
    doc = Document(text=json.dumps(profile), metadata={"source": "mock_linkedin"})
    nodes = SentenceSplitter(chunk_size=config.CHUNK_SIZE).get_nodes_from_documents([doc])
    print(f"Nodes: {len(nodes)}")

    # --- VectorStoreIndex: embed + store in one step ---
    print("Building index...")
    index = VectorStoreIndex(nodes, show_progress=True)
    print(f"Indexed: {len(index.index_struct.nodes_dict)} node(s)\n")

    # --- Retriever: search only, no LLM answer ---
    query = "What company did they work for on RAG migration?"
    print(f"Retriever query: {query}")
    retriever = index.as_retriever(similarity_top_k=config.SIMILARITY_TOP_K)
    hits = retriever.retrieve(query)
    for rank, hit in enumerate(hits, start=1):
        snippet = hit.node.get_text()[:100].replace("\n", " ")
        print(f"  [{rank}] score={hit.score:.4f} | {snippet}...")
    print(f"  (top_k={config.SIMILARITY_TOP_K}, but only {len(nodes)} node(s) exist)\n")

    # --- Query engine: retrieve + LLM ---
    question = "What skills are listed on the profile?"
    print(f"Query engine question: {question}")
    engine = index.as_query_engine(
        similarity_top_k=config.SIMILARITY_TOP_K,
        text_qa_template=PromptTemplate(config.USER_QUESTION_TEMPLATE),
    )
    print(f"Answer: {engine.query(question)}\n")

    # --- Prompt templates (05.pdf config.py) ---
    print("Templates use {context_str} and {query_str}:")
    print(config.USER_QUESTION_TEMPLATE[:120], "...")


if __name__ == "__main__":
    main()