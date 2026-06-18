"""Capstone 01A — REFERENCE / answer key (peek only after you tried the bites).

You type: capstone_01_ingest.py
Notebook: playground/notebooks/sean_capstone01_ingest_lab.ipynb

Load one PDF at a time from a local path or URL. Re-runs skip unchanged files.
Same chunk/embedding settings must match capstone_01_chat.py.

Pre-read: capstone/capstone01.md · corpus list: capstone/corpus_sources.json

Run set_env.ps1 + network (embeddings; URL fetch if remote).

Examples:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\capstone\\capstone_01_ingest_reference.py
    python .\\capstone\\capstone_01_ingest_reference.py --list
    python .\\capstone\\capstone_01_ingest_reference.py --corpus
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

_LANGCHAIN_ROOT = Path(__file__).resolve().parent.parent
if str(_LANGCHAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(_LANGCHAIN_ROOT))

from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from watson_llm import make_watsonx_embeddings

DEFAULT_SOURCE = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "96-FDF8f7coh0ooim7NyEQ/langchain-paper.pdf"
)

CHROMA_DIR = Path(__file__).resolve().parent / "data" / "chroma_01"
MANIFEST_PATH = Path(__file__).resolve().parent / "data" / "ingest_manifest.json"
CORPUS_PATH = Path(__file__).resolve().parent / "corpus_sources.json"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
METADATA_SOURCE_KEY = "ingest_source_id"

EMBED_PARAMS = {
    EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
    EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
}


def is_url(source: str) -> bool:
    parsed = urlparse(source)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def normalize_source(source: str) -> str:
    """Stable key for manifest + Chroma metadata (absolute path or canonical URL)."""
    if is_url(source):
        return source.strip()
    return str(Path(source).expanduser().resolve())


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_pdf_bytes(source: str) -> tuple[bytes, str]:
    """Return raw PDF bytes and the path/URL PyPDFLoader should use."""
    if is_url(source):
        with urlopen(source, timeout=120) as response:
            data = response.read()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp.write(data)
        tmp.close()
        return data, tmp.name

    path = Path(source).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")
    return path.read_bytes(), str(path)


def load_manifest() -> dict:
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
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")


def manifest_entry(manifest: dict, source_id: str) -> dict | None:
    return manifest.get("sources", {}).get(source_id)


def chroma_has_data() -> bool:
    return CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir())


def make_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def tag_chunks(chunks: list, source_id: str, title: str | None) -> list:
    for chunk in chunks:
        chunk.metadata[METADATA_SOURCE_KEY] = source_id
        if title:
            chunk.metadata["ingest_title"] = title
    return chunks


def load_and_split(source: str, loader_path: str) -> list:
    documents = PyPDFLoader(loader_path).load()
    return make_splitter().split_documents(documents)


def open_vector_store(embedding_model) -> Chroma | None:
    if not chroma_has_data():
        return None
    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding_model,
    )


def delete_source_chunks(vector_store: Chroma, source_id: str) -> None:
    try:
        vector_store._collection.delete(where={METADATA_SOURCE_KEY: source_id})
    except Exception as exc:
        print(f"Warning: could not delete prior chunks for {source_id}: {exc}")


def ingest_source(
    source: str,
    *,
    title: str | None = None,
    force: bool = False,
    quiet_skip: bool = False,
) -> str:
    """Ingest one PDF. Returns status: ingested | skipped | updated."""
    source_id = normalize_source(source)
    pdf_bytes, loader_path = read_pdf_bytes(source)
    content_hash = sha256_bytes(pdf_bytes)

    manifest = load_manifest()
    prior = manifest_entry(manifest, source_id)

    if prior and prior.get("content_hash") == content_hash and not force:
        if not quiet_skip:
            print(f"Skip (unchanged): {title or source_id}")
            print(f"  hash: {content_hash[:12]}…  chunks: {prior.get('chunk_count', '?')}")
        return "skipped"

    action = "updated" if prior else "ingested"
    if prior and prior.get("content_hash") != content_hash:
        print(f"Re-ingest (content changed): {title or source_id}")
    elif force and prior:
        print(f"Re-ingest (--force): {title or source_id}")
    else:
        print(f"Ingest: {title or source_id}")

    chunks = load_and_split(source, loader_path)
    tag_chunks(chunks, source_id, title)
    print(f"  chunks: {len(chunks)}")

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    embedding_model = make_watsonx_embeddings(EMBED_PARAMS)
    vector_store = open_vector_store(embedding_model)

    if vector_store is None:
        Chroma.from_documents(
            chunks,
            embedding_model,
            persist_directory=str(CHROMA_DIR),
        )
    else:
        if prior or force:
            delete_source_chunks(vector_store, source_id)
        vector_store.add_documents(chunks)

    manifest.setdefault("sources", {})[source_id] = {
        "title": title or Path(source_id).name,
        "content_hash": content_hash,
        "chunk_count": len(chunks),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "original": source if source != source_id else source_id,
    }
    save_manifest(manifest)

    print(f"  → {action} · manifest: {MANIFEST_PATH}")
    print(f"  → chroma: {CHROMA_DIR}")
    return action


def cmd_list() -> None:
    manifest = load_manifest()
    sources = manifest.get("sources", {})
    if not sources:
        print("No sources ingested yet.")
        print(f"Try: python capstone_01_ingest_reference.py {DEFAULT_SOURCE}")
        return

    print(f"Ingested sources ({len(sources)}):")
    for source_id, meta in sources.items():
        title = meta.get("title", source_id)
        chunks = meta.get("chunk_count", "?")
        ingested_at = meta.get("ingested_at", "?")
        print(f"  • {title}")
        print(f"    id: {source_id}")
        print(f"    chunks: {chunks}  at: {ingested_at}")


def cmd_corpus(force: bool) -> None:
    if not CORPUS_PATH.exists():
        print(f"Missing corpus file: {CORPUS_PATH}")
        sys.exit(1)

    with CORPUS_PATH.open(encoding="utf-8") as fh:
        corpus = json.load(fh)

    results = {"ingested": 0, "updated": 0, "skipped": 0, "failed": 0}
    for item in corpus.get("sources", []):
        url = item["url"]
        title = item.get("title", item.get("id", url))
        try:
            status = ingest_source(url, title=title, force=force, quiet_skip=True)
            results[status] = results.get(status, 0) + 1
            if status == "skipped":
                print(f"Skip (unchanged): {title}")
        except Exception as exc:
            results["failed"] += 1
            print(f"Failed: {title} — {exc}")

    print(
        "Corpus run:",
        f"ingested={results['ingested']}",
        f"updated={results['updated']}",
        f"skipped={results['skipped']}",
        f"failed={results['failed']}",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Consume a PDF (local path or URL) into capstone Chroma with dedupe.",
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
        help="Show manifest of already-ingested sources",
    )
    parser.add_argument(
        "--corpus",
        action="store_true",
        help="Ingest tiered PDFs from corpus_sources.json (skips dupes)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-embed even when content hash unchanged",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.list:
        cmd_list()
        return

    if args.corpus:
        cmd_corpus(force=args.force)
        return

    source = args.source or DEFAULT_SOURCE
    ingest_source(source, force=args.force)


if __name__ == "__main__":
    main()