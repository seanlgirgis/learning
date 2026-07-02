"""M3 Step 07 — prompt templates (05.pdf Part 1, quiz Q5).

Run:
  python steps/07_prompt_templates.py
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import m3_config as config
from lib.m3_shared import facts_prompt, question_prompt


def main() -> None:
    print("INITIAL_FACTS_TEMPLATE placeholders: {context_str}")
    print(config.INITIAL_FACTS_TEMPLATE[:200], "...\n")

    print("USER_QUESTION_TEMPLATE placeholders: {context_str}, {query_str}")
    print(config.USER_QUESTION_TEMPLATE[:200], "...\n")

    sample_context = "Jordan Lee works at Northwind Analytics."
    sample_query = "Where do they work?"
    filled = question_prompt().format(context_str=sample_context, query_str=sample_query)
    print("Filled USER template preview:")
    print(filled)
    print("\nCustomize via text_qa_template= in as_query_engine() — not forbidden.")


if __name__ == "__main__":
    main()