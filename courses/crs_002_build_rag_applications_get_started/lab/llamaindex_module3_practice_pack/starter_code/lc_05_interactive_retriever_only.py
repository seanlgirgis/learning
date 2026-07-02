"""LangChain interactive retriever-only search.

No LLM answer generation.
Good for cheap/local evidence finding.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

import lc_config


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

    print("LangChain retriever-only search.")
    print("Type 'exit' or 'quit' to stop.")
    print()

    while True:
        question = input("Question> ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        results = vector_store.similarity_search_with_score(question, k=3)

        for rank, (doc, score) in enumerate(results, start=1):
            print("=" * 80)
            print(f"RESULT {rank}")
            print("Score:", score)
            print("Source:", doc.metadata.get("source"))
            print()
            print(doc.page_content[:900])
            print()


if __name__ == "__main__":
    main()
