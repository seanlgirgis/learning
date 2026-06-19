"""Capstone 01A — Ingest (you build with Grok, bite by bite).

Consume a PDF or web page (local path or URL) into Chroma on disk. Skip duplicates via manifest.

Shared config: capstone/capstone_shared.py (also used by capstone_01_chat.py)

Guide:     capstone/capstone01.md
Notebook:  playground/notebooks/sean_capstone01_ingest_lab.ipynb
Reference: capstone_01_ingest_reference.py  (peek only after you try)

Run:
    cd D:\\Workarea\\learning\\playground\\langchain\\capstone
    python capstone_01_ingest.py --corpus
    python capstone_01_ingest.py --web
    python capstone_01_ingest.py --list

Needs: set_env.ps1 + network for embeddings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from capstone_shared import (
    CHROMA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    CORPUS_PATH,
    DEFAULT_SOURCE,
    MANIFEST_PATH,
    METADATA_SOURCE_KEY,
    make_embedding_model,
    open_vector_store,
)

# --- Bite 2: source + hash helpers ---
def is_url(source: str) -> bool:
    parsed = urlparse(source)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def normalize_source(source: str) -> str:
    if is_url(source):
        return source.strip()
    return str(Path(source).expanduser().resolve())


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_pdf_source(source: str) -> bool:
    """True for local ``.pdf`` paths and URLs whose path ends with ``.pdf``."""
    source_id = normalize_source(source)
    if is_url(source_id):
        return urlparse(source_id).path.lower().endswith(".pdf")
    return Path(source_id).suffix.lower() == ".pdf"


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


def read_web_bytes(source: str) -> bytes:
    """Fetch page bytes for manifest hash (web sources only)."""
    source_id = normalize_source(source)
    if not is_url(source_id):
        raise ValueError(f"Web ingest requires an http(s) URL: {source_id}")
    with urlopen(source_id, timeout=120) as response:
        return response.read()


def read_source_bytes(source: str) -> tuple[bytes, str | None, str]:
    """Return ``(hash_bytes, loader_path, kind)`` where kind is ``pdf`` or ``web``."""
    if is_pdf_source(source):
        raw, loader_path = read_pdf_bytes(source)
        return raw, loader_path, "pdf"
    raw = read_web_bytes(source)
    return raw, None, "web"


# --- Bite 3: manifest read/write + skip check in ingest_source ---
def load_manifest() -> dict:
    """Load ingest ledger from disk, or return empty structure on first run."""
    if not MANIFEST_PATH.exists():
        return {
            "version": 1,
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP,
            "sources": {},
        }
    with MANIFEST_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def save_manifest(manifest: dict) -> None:
    """Write ingest ledger to ingest_manifest.json."""
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")


def ingest_source(
    source: str,
    *,
    title: str | None = None,
    force: bool = False,
    quiet_skip: bool = False,
) -> str:
    """Ingest one PDF or web page: skip, or load/split/embed/persist to Chroma + manifest.

    Returns: ``skipped`` | ``ingested`` | ``updated``.
    """
    source_id = normalize_source(source)
    raw, loader_path, source_kind = read_source_bytes(source)
    content_hash = sha256_bytes(raw)

    manifest = load_manifest()
    prior = manifest.get("sources", {}).get(source_id)

    display = title or prior.get("title") if prior else title or source_id

    if prior and prior.get("content_hash") == content_hash and not force:
        if not quiet_skip:
            print(f"Skip (unchanged): {prior.get('title', display)}")
            print(f"  id: {source_id}")
            print(f"  hash: {content_hash[:12]}…  chunks: {prior.get('chunk_count', '?')}")
        return "skipped"

    action = "updated" if prior else "ingested"
    if prior and prior.get("content_hash") != content_hash:
        print(f"Re-ingest (content changed): {display}")
    elif force and prior:
        print(f"Re-ingest (--force): {display}")
    else:
        print(f"Ingest: {display}")

    print(f"  kind: {source_kind}  bytes: {len(raw)}  hash: {content_hash[:16]}...")
    if loader_path:
        print(f"  loader_path: {loader_path}")

    chunks = load_and_split(source_id, source_kind, loader_path)
    print(f"  chunks: {len(chunks)}")

    persist_chunks_to_chroma(chunks, source_id=source_id, prior=prior, force=force)

    manifest.setdefault("sources", {})[source_id] = {
        "title": title or Path(source_id).name,
        "kind": source_kind,
        "content_hash": content_hash,
        "chunk_count": len(chunks),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    save_manifest(manifest)

    print(f"  → {action} · manifest: {MANIFEST_PATH}")
    print(f"  → chroma: {CHROMA_DIR}")
    return action


# --- Bite 4: load + split ---
def make_splitter() -> RecursiveCharacterTextSplitter:
    """Build the text splitter used for all capstone ingests."""
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def tag_chunks(chunks: list, source_id: str) -> list:
    """Stamp each chunk with canonical ``ingest_source_id``."""
    for chunk in chunks:
        chunk.metadata[METADATA_SOURCE_KEY] = source_id
    return chunks


def load_and_split(source_id: str, source_kind: str, loader_path: str | None) -> list:
    """Load PDF or web page, split into chunks, tag with ``source_id``."""
    if source_kind == "pdf":
        if not loader_path:
            raise ValueError("PDF ingest requires loader_path")
        pages = PyPDFLoader(loader_path).load()
    else:
        pages = WebBaseLoader(source_id).load()
    chunks = make_splitter().split_documents(pages)
    return tag_chunks(chunks, source_id)


# --- Bite 5: Chroma persist (uses capstone_shared for paths + embed model) ---
def delete_source_chunks(vector_store: Chroma, source_id: str) -> None:
    """Remove all chunks for one source before re-ingest (changed file or --force)."""
    try:
        vector_store._collection.delete(where={METADATA_SOURCE_KEY: source_id})
    except Exception as exc:
        print(f"  warning: could not delete prior chunks: {exc}")


def persist_chunks_to_chroma(
    chunks: list,
    *,
    source_id: str,
    prior: dict | None,
    force: bool,
) -> None:
    """Embed chunks with Watsonx and write to persisted Chroma."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    embedding_model = make_embedding_model()
    vector_store = open_vector_store(embedding_model)

    if vector_store is None:
        Chroma.from_documents(
            chunks,
            embedding_model,
            persist_directory=str(CHROMA_DIR),
        )
        return

    if prior or force:
        delete_source_chunks(vector_store, source_id)
    vector_store.add_documents(chunks)


# --- Bite 6: CLI + corpus batch ---
def cmd_web(*, force: bool = False) -> None:
    """Ingest every URL in corpus_sources.json ``web_phase2``, skipping unchanged sources."""
    if not CORPUS_PATH.exists():
        print(f"Missing corpus file: {CORPUS_PATH}")
        sys.exit(1)

    with CORPUS_PATH.open(encoding="utf-8") as fh:
        corpus = json.load(fh)

    counts: dict[str, int] = {}
    for item in corpus.get("web_phase2", []):
        url = item["url"]
        doc_title = item.get("title", item.get("id", url))
        try:
            status = ingest_source(
                url,
                title=doc_title,
                force=force,
                quiet_skip=True,
            )
            counts[status] = counts.get(status, 0) + 1
            if status == "skipped":
                print(f"Skip (unchanged): {doc_title}")
        except Exception as exc:
            counts["failed"] = counts.get("failed", 0) + 1
            print(f"Failed: {doc_title} — {exc}")

    print(
        "Web run:",
        f"ingested={counts.get('ingested', 0)}",
        f"updated={counts.get('updated', 0)}",
        f"skipped={counts.get('skipped', 0)}",
        f"failed={counts.get('failed', 0)}",
    )


def cmd_corpus(*, force: bool = False) -> None:
    """Ingest every PDF in corpus_sources.json, skipping unchanged sources."""
    if not CORPUS_PATH.exists():
        print(f"Missing corpus file: {CORPUS_PATH}")
        sys.exit(1)

    with CORPUS_PATH.open(encoding="utf-8") as fh:
        corpus = json.load(fh)

    counts: dict[str, int] = {}
    for item in corpus.get("sources", []):
        url = item["url"]
        doc_title = item.get("title", item.get("id", url))
        try:
            status = ingest_source(
                url,
                title=doc_title,
                force=force,
                quiet_skip=True,
            )
            counts[status] = counts.get(status, 0) + 1
            if status == "skipped":
                print(f"Skip (unchanged): {doc_title}")
        except Exception as exc:
            counts["failed"] = counts.get("failed", 0) + 1
            print(f"Failed: {doc_title} — {exc}")

    print(
        "Corpus run:",
        f"ingested={counts.get('ingested', 0)}",
        f"updated={counts.get('updated', 0)}",
        f"skipped={counts.get('skipped', 0)}",
        f"failed={counts.get('failed', 0)}",
    )


def cmd_list() -> None:
    """Print sources recorded in the ingest manifest (--list)."""
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


def build_parser() -> argparse.ArgumentParser:
    """Build CLI: source, --list, --corpus, --web, --force."""
    parser = argparse.ArgumentParser(
        description="Capstone 01 ingest — consume PDFs and web pages into Chroma.",
    )
    parser.add_argument("source", nargs="?", default=None, help="PDF path, PDF URL, or web URL")
    parser.add_argument("--list", action="store_true", help="Show manifest entries")
    parser.add_argument("--corpus", action="store_true", help="Ingest corpus_sources.json PDFs")
    parser.add_argument("--web", action="store_true", help="Ingest corpus_sources.json web_phase2")
    parser.add_argument("--force", action="store_true", help="Re-embed even if unchanged")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.list:
        cmd_list()
        return

    if args.corpus:
        cmd_corpus(force=args.force)
        return

    if args.web:
        cmd_web(force=args.force)
        return

    source = args.source or DEFAULT_SOURCE
    ingest_source(source, force=args.force)


if __name__ == "__main__":
    main()