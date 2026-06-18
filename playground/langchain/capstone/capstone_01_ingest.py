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


# --- Bite 1: imports + paths + constants ---
import argparse
import json
import sys
from pathlib import Path
import hashlib
import tempfile
from urllib.parse import urlparse
from urllib.request import urlopen


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


# --- Bite 2: source + hash helpers ---
# TODO: is_url, normalize_source, read_pdf_bytes, sha256_bytes
def is_url(source: str) -> bool:
    parsed = urlparse(source)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

def normalize_source(source: str) -> str:
    if is_url(source):
        return source.strip()
    return str(Path(source).expanduser().resolve())

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def read_pdf_bytes(source: str) -> tuple[bytes, str]:
    source_id = normalize_source(source)

    if is_url(source_id):
        with urlopen(source_id, timeout=120) as response:
            data = response.read()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp.write(data)
        tmp.close()
        return data, tmp.name

    path = Path(source_id)
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")
    return path.read_bytes(), str(path)

# --- Bite 3: manifest + dedupe ---
def load_manifest() -> dict:
    """
        Load the ingest ledger from disk, or return an empty one if missing.
        The manifest records which sources were embedded (by source_id and
        content_hash). Used for dedupe at ingest; not used at query time.
    """
    if not MANIFEST_PATH.exists():
        return {"version": 1, "sources": {}}
    with MANIFEST_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


# TODO: save_manifest, skip-if-unchanged in ingest_source


# --- Bite 4: load + split ---
# TODO: PyPDFLoader, RecursiveCharacterTextSplitter, tag chunk metadata


# --- Bite 5: Chroma persist ---
# TODO: make_watsonx_embeddings, from_documents or add_documents


# --- Bite 6: CLI (shell now; full ingest_source later) ---
def cmd_list() -> None:
    manifest = load_manifest()
    sources = manifest.get("sources", {})
    if not sources:
        print("No sources ingested yet.")
        return
    print(f"Ingested sources ({len(sources)}):")
    for source_id, meta in sources.items():
        title = meta.get("title", source_id)
        chunks = meta.get("chunk_count", "?")
        print(f"  • {title}  chunks={chunks}")
        print(f"    id: {source_id}")


def cmd_probe(source: str) -> None:
    """Temporary: read + hash only until bites 4–5 wire Chroma."""
    raw, loader_path = read_pdf_bytes(source)
    print("source_id:", normalize_source(source))
    print("bytes:", len(raw))
    print("hash:", sha256_bytes(raw)[:16], "...")
    print("loader_path:", loader_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Capstone 01 ingest — consume PDFs into Chroma (building bite by bite).",
    )
    parser.add_argument(
        "source",
        nargs="?",
        default=None,
        help="PDF file path or URL (default: LangChain course paper)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Show ingest_manifest.json entries",
    )
    parser.add_argument(
        "--corpus",
        action="store_true",
        help="Ingest all PDFs in corpus_sources.json (not wired yet)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-embed even if unchanged (not wired yet)",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.list:
        cmd_list()
        return

    if args.corpus:
        raise NotImplementedError("Bite 5–6: wire --corpus after Chroma ingest exists.")

    source = args.source or DEFAULT_SOURCE
    if args.force:
        print("Note: --force will matter once full ingest_source exists.")
    cmd_probe(source)


if __name__ == "__main__":
    main()