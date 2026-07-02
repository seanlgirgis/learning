"""
Lab 3: Chroma Native Embedding Search

Goal:
Let Chroma create embeddings internally instead of manually calling
SentenceTransformer ourselves.
"""

import chromadb


def main() -> None:
    documents = [
        "Software developers fix coding mistakes called bugs in applications.",
        "Debugging is the process of finding and fixing errors in code.",
        "Garden plants can be damaged by insects, mildew, or poor soil conditions.",
        "Baking paper is often called parchment paper in North America.",
    ]

    ids = [
        "doc_software_bug",
        "doc_debugging",
        "doc_garden",
        "doc_baking_paper",
    ]

    query = "Who is responsible for fixing coding mistakes?"

    print("LAB 3: CHROMA NATIVE EMBEDDING SEARCH")
    print("=" * 50)
    print(f"Query: {query}")

    client = chromadb.Client()

    collection = client.create_collection(
        name="mini_chroma_native_lab"
    )

    collection.add(
        ids=ids,
        documents=documents,
    )

    results = collection.query(
        query_texts=[query],
        n_results=3,
    )

    print("\nRESULTS")
    print("-" * 50)

    for rank, doc_text in enumerate(results["documents"][0], start=1):
        doc_id = results["ids"][0][rank - 1]
        distance = results["distances"][0][rank - 1]

        print(f"\nRank {rank}: {doc_id}")
        print(f"Distance: {distance:.4f}")
        print(f"Text: {doc_text}")


if __name__ == "__main__":
    main()