"""Shared M1 ingest helpers — used by 02–07 scripts."""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

_LANGCHAIN = Path(__file__).resolve().parents[4] / "playground" / "langchain"
if str(_LANGCHAIN) not in sys.path:
    sys.path.insert(0, str(_LANGCHAIN))

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from watson_llm import make_watsonx_embeddings, make_watsonx_llm


POLICIES_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "6JDbUb_L3egv_eOkouY71A.txt"
)
PRACTICE_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "XVnuuEg94sAE4S_xAsGxBA.txt"
)

DATA_DIR = Path(__file__).resolve().parent / "_data"


def ensure_text_file(url: str, filename: str) -> Path:
    """Download once into _data/, validate non-empty, return path."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / filename
    if not path.is_file():
        print(f"Downloading {filename} ...")
        urllib.request.urlretrieve(url, path)
    else:
        print(f"Using cached: {path}")
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(f"Error: file missing or empty: {path}")
    print(f"OK — {path.stat().st_size} bytes")
    return path


def build_chroma_from_txt(path: Path) -> Chroma:
    """Load → split → embed → in-memory Chroma (M1 notebook pattern)."""
    loader = TextLoader(str(path), encoding="utf-8")
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = splitter.split_documents(documents)
    print("Chunks:", len(texts))
    embeddings = make_watsonx_embeddings()
    docsearch = Chroma.from_documents(texts, embeddings)
    print("Chroma ingest OK")
    return docsearch


def make_llm():
    return make_watsonx_llm()