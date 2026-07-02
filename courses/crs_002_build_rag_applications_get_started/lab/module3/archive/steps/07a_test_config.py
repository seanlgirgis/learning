"""M3 Step 07a — test_config.py mirror (05.pdf Part 1).

Run:
  python steps/07a_test_config.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib import m3_config as config


def main() -> None:
    print("=== RAG knobs ===")
    print(f"CHUNK_SIZE: {config.CHUNK_SIZE}")
    print(f"SIMILARITY_TOP_K: {config.SIMILARITY_TOP_K}")

    print("\n=== INITIAL_FACTS_TEMPLATE ===")
    print(f"has context_str: {'{context_str}' in config.INITIAL_FACTS_TEMPLATE}")
    print(config.INITIAL_FACTS_TEMPLATE.strip())

    print("\n=== USER_QUESTION_TEMPLATE ===")
    print(f"has context_str: {'{context_str}' in config.USER_QUESTION_TEMPLATE}")
    print(f"has query_str: {'{query_str}' in config.USER_QUESTION_TEMPLATE}")
    print(config.USER_QUESTION_TEMPLATE.strip())


if __name__ == "__main__":
    main()