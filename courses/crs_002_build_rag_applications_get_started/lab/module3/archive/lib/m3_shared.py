"""Shared helpers for Module 3 step scripts (OpenAI backend)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from llama_index.core import Document, PromptTemplate, Settings, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from lib import m3_config as config

MODULE_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = MODULE_ROOT / "data"
MOCK_PROFILE_PATH = DATA_DIR / "mock_linkedin_profile.json"
SAMPLE_DOCS_DIR = DATA_DIR / "sample_docs"


def require_openai() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY missing — run set_env.ps1 first.")


def configure_settings(*, temperature: float = 0.0) -> None:
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    embed = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    Settings.llm = OpenAI(model=model, temperature=temperature)
    Settings.embed_model = OpenAIEmbedding(model=embed)


def load_mock_profile(path: Path = MOCK_PROFILE_PATH) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Mock profile not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def profile_to_nodes(profile_data: dict[str, Any], chunk_size: int | None = None):
    text = json.dumps(profile_data)
    doc = Document(text=text, metadata={"source": "mock_linkedin"})
    splitter = SentenceSplitter(chunk_size=chunk_size or config.CHUNK_SIZE)
    return splitter.get_nodes_from_documents([doc])


def build_index_from_nodes(nodes) -> VectorStoreIndex:
    return VectorStoreIndex(nodes, show_progress=True)


def verify_embeddings(index: VectorStoreIndex) -> tuple[int, int]:
    """05.pdf Part 4 — confirm each indexed node has a stored embedding."""
    node_ids = list(index.index_struct.nodes_dict.keys())
    missing: list[str] = []
    for node_id in node_ids:
        try:
            embedding = index.vector_store.get(node_id)
        except Exception:
            embedding = None
        if embedding is None:
            missing.append(node_id)
    return len(node_ids), len(missing)


def build_index_from_profile(profile: dict[str, Any]) -> VectorStoreIndex:
    nodes = profile_to_nodes(profile)
    return build_index_from_nodes(nodes)


def facts_prompt() -> PromptTemplate:
    return PromptTemplate(config.INITIAL_FACTS_TEMPLATE)


def question_prompt() -> PromptTemplate:
    return PromptTemplate(config.USER_QUESTION_TEMPLATE)


def make_query_engine(index: VectorStoreIndex, *, template: PromptTemplate, top_k: int | None = None):
    return index.as_query_engine(
        similarity_top_k=top_k or config.SIMILARITY_TOP_K,
        text_qa_template=template,
    )


def generate_initial_facts(index: VectorStoreIndex) -> str:
    engine = make_query_engine(index, template=facts_prompt())
    response = engine.query(
        "Provide three interesting facts about this person's career or education."
    )
    return str(response)


def answer_question(index: VectorStoreIndex, question: str) -> str:
    engine = make_query_engine(index, template=question_prompt())
    return str(engine.query(question))