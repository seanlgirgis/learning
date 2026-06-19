"""Capstone 01 — debug retrieval only (no LLM).

Print which chunks Chroma returns for a question. Use before blaming the chat prompt.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain\\capstone
    python debug_retrieval.py "What is lost in the middle problem for LLMs?"
    python debug_retrieval.py
"""

from __future__ import annotations

import math
import sys

from capstone_shared import chroma_has_data, load_vector_store, make_embedding_model

# Match capstone_01_chat.py retriever settings
SEARCH_TYPE = "mmr"
SEARCH_KWARGS = {"k": 5, "fetch_k": 20}

PREVIEW_CHARS = 350


def require_chroma() -> None:
    if chroma_has_data():
        return
    print("No vector store. Run: python capstone_01_ingest.py --corpus")
    sys.exit(1)


def short_source(source_id: str) -> str:
    if not source_id:
        return "?"
    return source_id.rsplit("/", 1)[-1]


def build_retriever(vector_store):
    return vector_store.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs=SEARCH_KWARGS,
    )


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def print_hits(question: str, docs: list) -> None:
    print(f"Q: {question}")
    print(f"  retriever: {SEARCH_TYPE}  {SEARCH_KWARGS}")
    print(f"  hits: {len(docs)}")
    for i, doc in enumerate(docs, start=1):
        meta = doc.metadata
        src = short_source(meta.get("ingest_source_id", meta.get("source", "?")))
        page = meta.get("page", "?")
        preview = doc.page_content[:PREVIEW_CHARS].replace("\n", " ")
        if len(doc.page_content) > PREVIEW_CHARS:
            preview += "..."
        print(f"  [{i}] {src}  p{page}")
        print(f"      {preview}")


def compare_query_vectors(q1: str, q2: str) -> None:
    embed = make_embedding_model()
    v1 = embed.embed_query(q1)
    v2 = embed.embed_query(q2)
    print(f"cosine({q1!r}, {q2!r}) = {cosine(v1, v2):.4f}")
    if cosine(v1, v2) > 0.99:
        print("  warning: vectors nearly identical — check EMBED_PARAMS (truncate?)")


def debug_question(question: str, *, compare_to: str | None = None) -> None:
    retriever = build_retriever(load_vector_store())
    docs = retriever.invoke(question)
    print()
    print_hits(question, docs)
    if compare_to:
        print()
        compare_query_vectors(question, compare_to)
    print()


def main() -> None:
    require_chroma()

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:]).strip()
        debug_question(question)
        return

    print("Retrieval debug (empty line or 'quit' to exit)")
    print("Tip: ask two questions — if hits are identical, retrieval is suspect.")
    while True:
        question = input("Q: ").strip()
        if not question or question.lower() in ("quit", "exit"):
            break
        other = input("Compare cosine to (optional): ").strip()
        debug_question(question, compare_to=other or None)


if __name__ == "__main__":
    main()