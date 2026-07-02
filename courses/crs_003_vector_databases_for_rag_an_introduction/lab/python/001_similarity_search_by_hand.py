"""
001_similarity_search_by_hand.py

Tiny Lab 1: Similarity search with REAL computed vectors.

This replaces the earlier hand-made/fake vectors.

Preferred path:
    pip install sentence-transformers

Then run:
    python .\001_similarity_search_by_hand.py

What it proves:
    - Text documents are converted into numeric vectors.
    - A user question is converted into a numeric vector.
    - We compare the query vector to each document vector.
    - The closest documents rank first.

If sentence-transformers is not installed, the script falls back to scikit-learn
TF-IDF vectors if available. TF-IDF is real vectorization, but it is keyword-based,
not deep semantic embedding.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence, Tuple

Vector = Sequence[float]


@dataclass(frozen=True)
class Document:
    """A tiny document/chunk that we want to search."""

    doc_id: str
    text: str
    source: str


@dataclass(frozen=True)
class SearchResult:
    """One ranked search result."""

    rank: int
    doc: Document
    cosine_similarity: float
    euclidean_distance: float


def cosine_similarity(a: Vector, b: Vector) -> float:
    """Return cosine similarity. Higher means closer direction."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


def euclidean_distance(a: Vector, b: Vector) -> float:
    """Return Euclidean distance. Lower means closer position."""
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def load_embedding_model():
    """
    Load a real embedding/vectorization backend.

    First choice: sentence-transformers, a true local embedding model.
    Fallback: scikit-learn TF-IDF, a real keyword vectorizer.
    """
    try:
        from sentence_transformers import SentenceTransformer

        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        model = SentenceTransformer(model_name)
        return "sentence-transformers", model_name, model
    except Exception as sentence_transformer_error:
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer

            vectorizer = TfidfVectorizer(stop_words="english")
            return "tfidf", "sklearn TfidfVectorizer", vectorizer
        except Exception as tfidf_error:
            raise RuntimeError(
                "No embedding/vectorization backend is available.\n\n"
                "Preferred install:\n"
                "    pip install sentence-transformers\n\n"
                "Fallback install:\n"
                "    pip install scikit-learn\n\n"
                f"sentence-transformers error: {sentence_transformer_error}\n"
                f"scikit-learn error: {tfidf_error}"
            ) from tfidf_error


def embed_texts(texts: List[str]) -> Tuple[str, str, List[List[float]]]:
    """Convert text into numeric vectors using the selected backend."""
    backend, model_name, model = load_embedding_model()

    if backend == "sentence-transformers":
        vectors = model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        return backend, model_name, vectors.tolist()

    # Fallback: real TF-IDF vectors. This is not semantic like transformer embeddings,
    # but it is still real vectorization computed from the text.
    matrix = model.fit_transform(texts)
    return backend, model_name, matrix.toarray().tolist()


def rank_documents(query: str, documents: List[Document], top_k: int = 3) -> Tuple[str, str, List[SearchResult]]:
    """Embed query + docs, compare vectors, and return top results."""
    all_texts = [query] + [doc.text for doc in documents]
    backend, model_name, vectors = embed_texts(all_texts)

    query_vector = vectors[0]
    document_vectors = vectors[1:]

    scored: List[SearchResult] = []
    for doc, doc_vector in zip(documents, document_vectors):
        scored.append(
            SearchResult(
                rank=0,
                doc=doc,
                cosine_similarity=cosine_similarity(query_vector, doc_vector),
                euclidean_distance=euclidean_distance(query_vector, doc_vector),
            )
        )

    scored.sort(key=lambda item: item.cosine_similarity, reverse=True)

    ranked = [
        SearchResult(
            rank=index + 1,
            doc=result.doc,
            cosine_similarity=result.cosine_similarity,
            euclidean_distance=result.euclidean_distance,
        )
        for index, result in enumerate(scored[:top_k])
    ]

    return backend, model_name, ranked


def print_results(query: str, backend: str, model_name: str, results: Iterable[SearchResult]) -> None:
    """Pretty-print ranked search results."""
    print("TINY LAB 1: REAL VECTOR SIMILARITY SEARCH")
    print("=" * 55)
    print(f"Query: {query}")
    print(f"Vector backend: {backend}")
    print(f"Model/vectorizer: {model_name}")
    print()

    for result in results:
        print(f"Rank {result.rank}: {result.doc.doc_id}")
        print(f"  Cosine similarity:  {result.cosine_similarity:.4f}  higher is closer")
        print(f"  Euclidean distance: {result.euclidean_distance:.4f}  lower is closer")
        print(f"  Source: {result.doc.source}")
        print(f"  Text: {result.doc.text}")
        print()


def main() -> None:
    documents = [
        Document(
            doc_id="doc_software_bug",
            source="mini_docs/software.md",
            text="Software developers fix coding mistakes called bugs in applications.",
        ),
        Document(
            doc_id="doc_debugging",
            source="mini_docs/debugging.md",
            text="Debugging is the process of finding and fixing errors in code.",
        ),
        Document(
            doc_id="doc_insect_bug",
            source="mini_docs/insects.md",
            text="Beetles and ants are insects, and many people casually call insects bugs.",
        ),
        Document(
            doc_id="doc_garden",
            source="mini_docs/garden.md",
            text="Garden plants can be damaged by insects, mildew, or poor soil conditions.",
        ),
    ]

    query = "Who is responsible for fixing coding mistakes?"
    backend, model_name, results = rank_documents(query=query, documents=documents, top_k=3)
    print_results(query=query, backend=backend, model_name=model_name, results=results)


if __name__ == "__main__":
    main()
