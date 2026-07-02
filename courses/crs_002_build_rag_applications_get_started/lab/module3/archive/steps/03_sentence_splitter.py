"""M3 Step 03 — SentenceSplitter → nodes (01.md, quiz Q4).

Run:
  python steps/03_sentence_splitter.py
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

LONG_TEXT = (
    "Sentence one about policies.\n\n"
    "Sentence two about remote work. Managers approve up to three days.\n\n"
    "Sentence three about embeddings and retrieval for RAG pipelines."
)


def main() -> None:
    doc = Document(text=LONG_TEXT)
    # chunk_size is in TOKENS, not sentences. 40 tokens fits all 3 sentences → 1 node.
    splitter = SentenceSplitter(chunk_size=15, chunk_overlap=2)
    nodes = splitter.get_nodes_from_documents([doc])
    print(f"Nodes created: {len(nodes)} (3 sentences ≠ 3 nodes unless text exceeds chunk_size)")
    for i, node in enumerate(nodes, start=1):
        print('-' * 40)
        preview = node.get_text().replace("\n", " ")[:80]
        print(f"  [{i}] {preview!r}...")
    print("="* 100)
    print("\nSplits recursively on newlines/periods until chunk_size (tokens) fits.")


if __name__ == "__main__":
    main()