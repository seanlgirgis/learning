"""M3 Step 10 — generate_initial_facts + answer_user_query (05.pdf Part 6).

Run:
  python steps/10_facts_and_qa.py
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import m3_config as config
from lib.m3_shared import (
    answer_question,
    build_index_from_profile,
    configure_settings,
    generate_initial_facts,
    load_mock_profile,
    require_openai,
)


def main() -> None:
    require_openai()
    configure_settings()

    index = build_index_from_profile(load_mock_profile())

    print("=== Initial facts (icebreaker) ===")
    print(generate_initial_facts(index))

    print("\n=== Manual retrieve (05.pdf Part 6 teaching step) ===")
    q = "What are their interests outside work?"
    retriever = index.as_retriever(similarity_top_k=config.SIMILARITY_TOP_K)
    source_nodes = retriever.retrieve(q)
    context_str = "\n".join(n.node.get_text() for n in source_nodes)
    print(f"Retrieved {len(source_nodes)} chunks; context preview:")
    print(context_str[:300], "...\n")

    print("=== Sample Q&A via query engine ===")
    print(f"Q: {q}")
    print(f"A: {answer_question(index, q)}")


if __name__ == "__main__":
    main()