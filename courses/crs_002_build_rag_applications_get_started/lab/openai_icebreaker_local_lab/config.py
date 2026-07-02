"""Central settings for the local OpenAI Icebreaker Bot lab.

This file holds prompts, chunk sizes, and model names. It does not call OpenAI.

Coursera used IBM watsonx credentials; this local lab reads OpenAI settings from
the environment (or a ``.env`` file). The RAG pipeline steps stay the same — only
the provider changed.

Mental model:
    extraction settings → how we load profile data
    CHUNK_SIZE → how big each searchable node/chunk is
    SIMILARITY_TOP_K → how many chunks the retriever returns
    prompt templates → instructions sent to the LLM after retrieval
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the project folder (optional if you use set_env.ps1 instead).
load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent

# --- OpenAI credentials and models (no API calls happen in this file) ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_LLM_MODEL = (
    os.getenv("OPENAI_LLM_MODEL") or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
)
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# --- Generation and retrieval knobs ---
TEMPERATURE = 0.0  # 0 = more deterministic answers (good for profile Q&A)
MAX_TOKENS = 500
CHUNK_SIZE = 500  # tokens per node/chunk after splitting
SIMILARITY_TOP_K = 5  # top-k chunks passed into the prompt

# Proxycurl is only used when mock=False (real LinkedIn API fetch).
PROXYCURL_API_KEY = ""

# mock=True reads this file — no LinkedIn, no Proxycurl, no OpenAI.
MOCK_DATA_PATH = PROJECT_ROOT / "data" / "mock_linkedin_profile.json"

# Prompt templates use {context_str} (retrieved chunks) and {query_str} (question).
INITIAL_FACTS_TEMPLATE = """
You are an AI assistant helping generate professional networking icebreakers.
Use only the context below to answer.
Context:
{context_str}
Question:
{query_str}
Generate exactly three interesting facts about this person's career, education, or professional background.
Each fact should be one sentence.
Do not include facts that are not supported by the context.
Return only the numbered facts.
"""
USER_QUESTION_TEMPLATE = """
You are an AI assistant answering questions about a LinkedIn profile.
Use only the context below to answer.
If the answer is not available in the context, say "I don't know."
Context:
{context_str}
Question:
{query_str}
Answer:
"""