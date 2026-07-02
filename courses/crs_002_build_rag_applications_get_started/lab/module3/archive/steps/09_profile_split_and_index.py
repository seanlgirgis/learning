"""M3 Step 09 — split_profile_data + create_vector_database (05.pdf Part 4).

Run:
  python steps/09_profile_split_and_index.py
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.m3_shared import (
    build_index_from_profile,
    configure_settings,
    load_mock_profile,
    profile_to_nodes,
    require_openai,
    verify_embeddings,
)


def main() -> None:
    require_openai()
    configure_settings()

    profile = load_mock_profile()
    nodes = profile_to_nodes(profile)
    print(f"Nodes from profile: {len(nodes)}")
    for i, node in enumerate(nodes[:3], start=1):
        print(f"  node {i} preview: {node.get_text()[:100]}...")

    print("\nBuilding VectorStoreIndex...")
    index = build_index_from_profile(profile)
    print(f"Indexed node IDs: {len(index.index_struct.nodes_dict)}")

    total, missing = verify_embeddings(index)
    print(f"verify_embeddings: {total - missing}/{total} nodes have vectors")
    if missing:
        raise SystemExit(f"Missing embeddings for: {missing[:3]}")


if __name__ == "__main__":
    main()