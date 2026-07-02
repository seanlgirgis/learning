"""LLM interface import test — verify functions exist, do not call them.

OpenAI cost: **NONE** (import-only; no ``create_openai_*`` invocation).

Run::

    python tests/test_llm_interface_imports.py

Checks that provider-replacement helpers are wired before token-spending tests.
"""

import setup_imports  # noqa: F401
from modules.llm_interface import (
    change_llm_model,
    create_openai_embedding,
    create_openai_llm,
)

print("Imported create_openai_embedding:", callable(create_openai_embedding))
print("Imported create_openai_llm:", callable(create_openai_llm))
print("Imported change_llm_model:", callable(change_llm_model))