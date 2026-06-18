"""Capstone 01A — Ingest (you build with Grok, bite by bite).

Consume one PDF (local path or URL) into Chroma on disk. Skip duplicates via manifest.

Guide:     capstone/capstone01.md
Notebook:  playground/notebooks/sean_capstone01_ingest_lab.ipynb
Reference: capstone_01_ingest_reference.py  (peek only after you try)

Run (when bites are done):
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\capstone\\capstone_01_ingest.py
    python .\\capstone\\capstone_01_ingest.py --list

Interview spine:
    resolve source → hash bytes → check manifest → load/split → embed → persist

Bites (capstone01.md):
    1  paths + constants
    2  is_url, normalize_source, read_pdf_bytes, sha256_bytes
    3  load_manifest, save_manifest, skip if unchanged
    4  PyPDFLoader + splitter + ingest_source_id on chunks
    5  Chroma from_documents / add_documents
    6  argparse: source, --list, --corpus, --force

Needs: set_env.ps1 + network for embeddings.
"""

from __future__ import annotations
import sys
from pathlib import Path

_LANGCHAIN_ROOT = Path(__file__).resolve().parent.parent
if str(_LANGCHAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(_LANGCHAIN_ROOT))

_CAPSTONE = Path(__file__).resolve().parent
CHROMA_DIR = _CAPSTONE / "data" / "chroma_01"
MANIFEST_PATH = _CAPSTONE / "data" / "ingest_manifest.json"

DEFAULT_SOURCE = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "96-FDF8f7coh0ooim7NyEQ/langchain-paper.pdf"
)
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# --- Bite 1: imports + paths + constants ---
# TODOS


# --- Bite 2: source + hash helpers ---
# TODO: is_url, normalize_source, read_pdf_bytes, sha256_bytes


# --- Bite 3: manifest + dedupe ---
# TODO: load_manifest, save_manifest


# --- Bite 4: load + split ---
# TODO: PyPDFLoader, RecursiveCharacterTextSplitter, tag chunk metadata


# --- Bite 5: Chroma persist ---
# TODO: make_watsonx_embeddings, from_documents or add_documents


# --- Bite 6: CLI + orchestration ---
# TODO: ingest_source(), cmd_list(), argparse in main()


def main() -> None:
    print(_LANGCHAIN_ROOT)
#    raise NotImplementedError("Say 'ingest bite 1' in chat to start.")


if __name__ == "__main__":
    main()