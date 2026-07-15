"""
Lab 2: Similarity Search with Chroma DB

Goal:
Use Chroma as the vector database instead of manually storing vectors
and manually sorting similarities (see lab 001 for hand-scored cosine + L2).

Distance metric used in THIS lab: L2 (Euclidean) — Chroma's DEFAULT.

Why L2 here?
  - create_collection() is called with no hnsw "space" setting.
  - Chroma then uses space="l2" (not cosine, not inner product / dot).
  - Query results expose "distances" where LOWER = closer / more similar.

Compare later:
  - Lab 001 prints cosine (higher better) AND Euclidean (lower better) by hand.
  - Lab 004 sets cosine space explicitly on the collection.
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

    print("LAB 2: CHROMA SIMILARITY SEARCH")
    print("=" * 50)
    print(f"Query: {query}")
    # Chroma default space is L2 — lower distance = closer match.
    print("Distance metric: L2 (Euclidean) — Chroma default")
    print("  (lower distance = closer; we did not set space='cosine')")

    # --- Embed: still an explicit model call (same idea as production) ---
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    document_vectors = model.encode(
        documents,
        normalize_embeddings=True,
    ).tolist()

    query_vector = model.encode(
        [query],
        normalize_embeddings=True,
    ).tolist()[0]

    # --- Store + search: Chroma owns ranking (no hand cosine loop) ---
    client = chromadb.Client()

    # No configuration / metadata hnsw.space → DEFAULT distance = L2.
    # To use cosine instead you would configure space="cosine" (see lab 004).
    collection = client.create_collection(
        name="mini_similarity_lab"
    )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=document_vectors,  # we pass vectors we already computed
    )

    # Ordered nearest neighbors under the collection's distance space (here: L2).
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3,
    )

    print("\nRESULTS")
    print("-" * 50)

    for rank, doc_text in enumerate(results["documents"][0], start=1):
        doc_id = results["ids"][0][rank - 1]
        # L2 distance from Chroma: smaller number = more similar.
        distance = results["distances"][0][rank - 1]

        print(f"\nRank {rank}: {doc_id}")
        print(f"L2 distance: {distance:.4f}  (lower is closer)")






        print(f"Text: {doc_text}")


if __name__ == "__main__":
    main()