"""RAG pipeline modules for the local OpenAI Icebreaker Bot.

Package layout (same architecture as the Coursera LlamaIndex lab):

    data_extraction   → load profile data (extraction)
    data_processing   → Document → nodes/chunks → embeddings → index
    llm_interface     → OpenAI LLM + embedding clients (replaces watsonx)
    query_engine      → retriever + prompt + LLM → final answer

Importing any submodule runs ``bootstrap`` so ``config`` and ``modules`` resolve
when you run scripts from different folders.
"""

import bootstrap  # noqa: F401