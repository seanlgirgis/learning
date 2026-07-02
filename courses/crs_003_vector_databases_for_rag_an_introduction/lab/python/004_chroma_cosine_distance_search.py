"""
Lab 4: Chroma Similarity Search with Cosine Distance

Goal:
Tell Chroma explicitly to use cosine distance instead of the default distance.
"""

import chromadb
from sentence_transformers import SentenceTransformer


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

    print("LAB 4: CHROMA COSINE DISTANCE SEARCH")
    print("=" * 50)
    print(f"Query: {query}")

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    document_vectors = model.encode(
        documents,
        normalize_embeddings=True,
    ).tolist()

    query_vector = model.encode(
        [query],
        normalize_embeddings=True,
    ).tolist()[0]

    client = chromadb.Client()

    collection = client.create_collection(
        name="mini_similarity_lab_cosine",
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=document_vectors,
    )

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3,
    )

    print("\nRESULTS")
    print("-" * 50)

    for rank, doc_text in enumerate(results["documents"][0], start=1):
        doc_id = results["ids"][0][rank - 1]
        cosine_distance = results["distances"][0][rank - 1]
        estimated_cosine_similarity = 1 - cosine_distance

        print(f"\nRank {rank}: {doc_id}")
        print(f"Cosine distance: {cosine_distance:.4f}")
        print(f"Estimated cosine similarity: {estimated_cosine_similarity:.4f}")
        print(f"Text: {doc_text}")


if __name__ == "__main__":
    main()