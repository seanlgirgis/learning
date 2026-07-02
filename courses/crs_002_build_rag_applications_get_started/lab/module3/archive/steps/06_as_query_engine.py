"""M3 Step 06 — as_query_engine full RAG (02.md).

Run:
  python steps/06_as_query_engine.py
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.m3_shared import (
    answer_question,
    build_index_from_profile,
    configure_settings,
    load_mock_profile,
    require_openai,
)


def main() -> None:
    require_openai()
    configure_settings()

    index = build_index_from_profile(load_mock_profile())
    question = "What skills are listed on the profile?"
    print(f"Question: {question}\n")
    print(answer_question(index, question))
    print("\nOne .query() = embed + retrieve + augment + LLM (like M1 RetrievalQA.invoke).")


if __name__ == "__main__":
    main()