"""Shared configuration for LangChain local-embedding examples."""

from pathlib import Path
import os

PACK_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PACK_ROOT / "data" / "company_knowledge"
PERSIST_DIR = PACK_ROOT / "storage" / "langchain_chroma_company_knowledge"

LOCAL_EMBEDDING_MODEL = os.getenv(
    "LOCAL_EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))