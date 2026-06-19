"""Shared capstone 01 config and Chroma helpers — used by ingest and chat.

Import from here so CHROMA_DIR and embedding settings stay in one place.
"""

from __future__ import annotations

import sys
from pathlib import Path

_CAPSTONE_DIR = Path(__file__).resolve().parent
_LANGCHAIN_ROOT = _CAPSTONE_DIR.parent

if str(_LANGCHAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(_LANGCHAIN_ROOT))

from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from langchain_chroma import Chroma
from watson_llm import make_watsonx_embeddings

# --- paths (both scripts must use these) ---
CAPSTONE_DIR = _CAPSTONE_DIR
CHROMA_DIR = CAPSTONE_DIR / "data" / "chroma_01"
MANIFEST_PATH = CAPSTONE_DIR / "data" / "ingest_manifest.json"
CORPUS_PATH = CAPSTONE_DIR / "corpus_sources.json"

# --- ingest + retrieval alignment ---
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
METADATA_SOURCE_KEY = "ingest_source_id"

# Course labs use TRUNCATE_INPUT_TOKENS: 3 for tiny demos; capstone needs full text
# so queries and chunks embed with real semantic signal (truncate=3 makes every query identical).
EMBED_PARAMS = {
    EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
}

DEFAULT_SOURCE = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "96-FDF8f7coh0ooim7NyEQ/langchain-paper.pdf"
)


def chroma_has_data() -> bool:
    """Return True if the persist directory exists and is non-empty."""
    return CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir())


def make_embedding_model():
    """Watsonx embeddings with capstone ``EMBED_PARAMS`` (Route B)."""
    return make_watsonx_embeddings(EMBED_PARAMS)


def open_vector_store(embedding_model=None) -> Chroma | None:
    """Open existing Chroma on disk, or None if no ingest has run yet."""
    if not chroma_has_data():
        return None
    model = embedding_model or make_embedding_model()
    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=model,
    )


def load_vector_store() -> Chroma:
    """Load persisted Chroma for chat/query; raise if ingest not run."""
    if not chroma_has_data():
        raise FileNotFoundError(
            f"No vector store at {CHROMA_DIR}. Run capstone_01_ingest.py first."
        )
    store = open_vector_store()
    assert store is not None
    return store