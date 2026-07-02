"""Chunk profile data and build a searchable vector index.

Mental model — this file covers three RAG steps:

    Document  → one loaded text object (here: profile JSON as a string)
    node/chunk → smaller searchable pieces (``SentenceSplitter``)
    embedding  → semantic fingerprint per chunk (OpenAI, during indexing)
    index      → searchable memory (``VectorStoreIndex``)

Coursera used watsonx embeddings; this lab uses OpenAI embeddings. The LlamaIndex
classes (``Document``, ``VectorStoreIndex``) are the same.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from llama_index.core import Document, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

import config
from modules.llm_interface import create_openai_embedding

logger = logging.getLogger(__name__)


def split_profile_data(profile_data: Dict[str, Any]) -> List:
    """Turn profile JSON into LlamaIndex nodes (chunks).

    What it does:
        Serializes the profile dict to JSON, wraps it in a ``Document``, then
        splits it into node/chunk objects for embedding and retrieval.

    Inputs:
        profile_data: Dictionary from ``extract_linkedin_profile``.

    Returns:
        List of LlamaIndex nodes (chunks). Empty list on error.

    OpenAI:
        No — splitting is local text processing only.
    """
    try:
        profile_json = json.dumps(profile_data, indent=2)
        # Document = loaded text unit before chunking.
        document = Document(text=profile_json)
        splitter = SentenceSplitter(chunk_size=config.CHUNK_SIZE)
        nodes = splitter.get_nodes_from_documents([document])
        logger.info("Created %s nodes from profile data.", len(nodes))
        return nodes
    except Exception as exc:
        logger.error("Error in split_profile_data: %s", exc)
        return []


def create_vector_database(nodes: List) -> Optional[VectorStoreIndex]:
    """Embed chunks and store them in an in-memory vector index.

    What it does:
        Calls OpenAI embeddings for each node, then builds a ``VectorStoreIndex``
        (searchable memory for the retriever/query engine).

    Inputs:
        nodes: Chunk list from ``split_profile_data``.

    Returns:
        ``VectorStoreIndex`` on success, or ``None`` on error.

    OpenAI:
        Yes — embedding API calls happen inside ``VectorStoreIndex`` when nodes
        are embedded.
    """
    try:
        embedding_model = create_openai_embedding()
        index = VectorStoreIndex(
            nodes=nodes, embed_model=embedding_model, show_progress=True
        )
        logger.info("Vector database created successfully.")
        return index
    except Exception as exc:
        logger.error("Error in create_vector_database: %s", exc)
        return None


def verify_embeddings(index: VectorStoreIndex) -> bool:
    """Check that the index object looks ready for querying.

    What it does:
        Lightweight sanity check (index exists and has internal structure).
        Does not re-call OpenAI.

    Inputs:
        index: ``VectorStoreIndex`` from ``create_vector_database``.

    Returns:
        True if the index appears query-ready, else False.

    OpenAI:
        No — local object inspection only.
    """
    try:
        if index is None:
            logger.warning("Index is None.")
            return False
        if not hasattr(index, "index_struct"):
            logger.warning("Index does not expose index_struct.")
            return False
        logger.info("Vector index exists and is ready for querying.")
        return True
    except Exception as exc:
        logger.error("Error in verify_embeddings: %s", exc)
        return False