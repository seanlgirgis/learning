"""Config smoke test — print prompts, chunk size, and model names.

OpenAI cost: **NONE** (reads ``config.py`` only).

Run::

    python tests/test_config.py

Confirms templates and paths before you spend tokens on embedding tests.
"""

import setup_imports  # noqa: F401
import config

print("Initial Facts Template defined:", bool(config.INITIAL_FACTS_TEMPLATE))
print("User Question Template defined:", bool(config.USER_QUESTION_TEMPLATE))
print("Chunk Size:", config.CHUNK_SIZE)
print("Similarity Top K:", config.SIMILARITY_TOP_K)
print("OpenAI LLM Model:", config.OPENAI_LLM_MODEL)
print("OpenAI Embedding Model:", config.OPENAI_EMBEDDING_MODEL)
print("Mock Data Path:", config.MOCK_DATA_PATH)