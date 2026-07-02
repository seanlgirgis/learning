"""M3 Step 04 — VectorStoreIndex embed+store (02.md, quiz Q2).

Run:
  python steps/04_vector_store_index.py
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

from lib.m3_shared import configure_settings, require_openai


def main() -> None:
    require_openai()
    configure_settings()

    doc = Document(text="LlamaIndex stores embeddings and vectors in one VectorStoreIndex step.")
    nodes = SentenceSplitter(chunk_size=256, chunk_overlap=20).get_nodes_from_documents([doc])

    print("Building VectorStoreIndex (embed + store)...")
    from lib.m3_shared import build_index_from_nodes

    index = build_index_from_nodes(nodes)
    print(f"Index ready. Node count in struct: {len(index.index_struct.nodes_dict)}")
    print("LangChain M1 often: embed then Chroma.from_documents separately.")


if __name__ == "__main__":
    main()