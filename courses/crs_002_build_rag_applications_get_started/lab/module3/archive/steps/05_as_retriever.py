"""M3 Step 05 — as_retriever + similarity_top_k (02.md).

Run:
  python steps/05_as_retriever.py
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import m3_config as config
from lib.m3_shared import (
    build_index_from_profile,
    configure_settings,
    load_mock_profile,
    require_openai,
)


def main() -> None:
    require_openai()
    configure_settings()

    index = build_index_from_profile(load_mock_profile())
    retriever = index.as_retriever(similarity_top_k=config.SIMILARITY_TOP_K)

    query = "What company did they work for on RAG migration?"
    print(f"Query: {query}\n")
    results = retriever.retrieve(query)
    for rank, item in enumerate(results, start=1):
        print('-' * 80)
        snippet = item.node.get_text()[:120].replace("\n", " ")
        print(f"  [{rank}] score={item.score:.4f} | {snippet}...")


if __name__ == "__main__":
    main()