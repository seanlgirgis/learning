"""LangChain step 3: retriever-only search.

Stops before the LLM.
No LLM answer tokens.
Query embedding is local.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

import lc_config


QUESTIONS = [
    "What is the support escalation rule for Sev-1 incidents?",
    "Which product is better for dashboard-style reports?",
    "What changed after the May 2026 analytics outage?",
    "Can I upload API keys into an AI tool?",
    "Who is the CEO of Northwind Analytics?",
]


def main() -> None:
    if not lc_config.PERSIST_DIR.exists():
        raise SystemExit(
            "Persisted Chroma index not found. Run lc_02_build_local_chroma_index.py first."
        )

    embeddings = HuggingFaceEmbeddings(
        model_name=lc_config.LOCAL_EMBEDDING_MODEL
    )

    vector_store = Chroma(
        collection_name="company_knowledge",
        persist_directory=str(lc_config.PERSIST_DIR),
        embedding_function=embeddings,
    )

    for question in QUESTIONS:
        print("=" * 80)
        print("QUESTION:", question)
        print()

        results = vector_store.similarity_search_with_score(question, k=3)

        for rank, (doc, score) in enumerate(results, start=1):
            print(f"RESULT {rank}")
            print("Score:", score)
            print("Source:", doc.metadata.get("source"))
            print("Preview:")
            print(doc.page_content[:700])
            print("-" * 80)


if __name__ == "__main__":
    main()
