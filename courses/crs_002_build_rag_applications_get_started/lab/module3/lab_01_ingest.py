"""Module 3 — Lab 1: load text, split into nodes (01.md).

Run from lab/module3:
  python lab_01_ingest.py
"""

from __future__ import annotations

from pathlib import Path

from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

ROOT = Path(__file__).resolve().parent
SAMPLE_DOCS = ROOT / "data" / "sample_docs"

LONG_TEXT = (
    "Sentence one about policies.\n\n"
    "Sentence two about remote work. Managers approve up to three days.\n\n"
    "Sentence three about embeddings and retrieval for RAG pipelines."
)


def main() -> None:
    # --- 1. Document (whole source before chunking) ---
    doc = Document(
        text="Hello LlamaIndex",
        metadata={"source": "demo", "topic": "m3"},
    )
    print("1. Document")
    print(f"   id_: {doc.id_}")
    print(f"   metadata: {doc.metadata}")
    print(f"   text: {doc.text!r}\n")

    # --- 2. SimpleDirectoryReader (load files from a folder) ---
    print("2. SimpleDirectoryReader")
    for d in SimpleDirectoryReader(str(SAMPLE_DOCS)).load_data():
        print(f"   all files: {d.metadata.get('file_name')} ({len(d.text)} chars)")

    filtered = SimpleDirectoryReader(
        str(SAMPLE_DOCS),
        recursive=True,
        required_exts=[".csv", ".json"],
    ).load_data()
    for d in filtered:
        print(f"   csv/json only: {d.metadata.get('file_name')}")
    print("   quiz pattern: recursive=True + required_exts=['.csv', '.json']\n")

    # --- 3. SentenceSplitter (Document -> nodes) ---
    print("3. SentenceSplitter")
    splitter = SentenceSplitter(chunk_size=15, chunk_overlap=2)
    nodes = splitter.get_nodes_from_documents([Document(text=LONG_TEXT)])
    print(f"   nodes: {len(nodes)}  (chunk_size is tokens, not sentence count)")
    for i, node in enumerate(nodes, start=1):
        preview = node.get_text().replace("\n", " ")[:80]
        print(f"   [{i}] {preview!r}")


if __name__ == "__main__":
    main()