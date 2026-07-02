"""OpenAI model clients for the Icebreaker lab (provider replacement layer).

Coursera used IBM watsonx (``WatsonxLLM``, ``WatsonxEmbeddings``). This local lab
uses OpenAI adapters with the same LlamaIndex call pattern.

Mental model:
    embedding model → turns text into semantic fingerprints (vectors) for search
    LLM → writes the final natural-language answer from retrieved chunks

Compatibility aliases ``create_watsonx_*`` mirror Coursera function names so you
can map course notebooks to this project.
"""

import logging

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

import config

logger = logging.getLogger(__name__)


def require_openai_key() -> None:
    """Fail fast if ``OPENAI_API_KEY`` is missing.

    What it does:
        Raises before any paid OpenAI call is attempted.

    Inputs:
        None (reads ``config.OPENAI_API_KEY``).

    Returns:
        None.

    OpenAI:
        No — only checks configuration.
    """
    if not config.OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
        )


def create_openai_embedding() -> OpenAIEmbedding:
    """Build the OpenAI embedding client used for semantic search.

    What it does:
        Returns a LlamaIndex ``OpenAIEmbedding`` object for vectorizing chunks.

    Inputs:
        None (model name and API key come from ``config``).

    Returns:
        Configured ``OpenAIEmbedding`` instance.

    OpenAI:
        The client is created here; API calls happen later when the index embeds
        nodes (see ``create_vector_database``).
    """
    require_openai_key()
    embedding_model = OpenAIEmbedding(
        model=config.OPENAI_EMBEDDING_MODEL, api_key=config.OPENAI_API_KEY
    )
    logger.info("Created OpenAI embedding model: %s", config.OPENAI_EMBEDDING_MODEL)
    return embedding_model


def create_openai_llm(
    temperature: float = config.TEMPERATURE, max_tokens: int = config.MAX_TOKENS
) -> OpenAI:
    """Build the OpenAI LLM client used for answer generation.

    What it does:
        Returns a LlamaIndex ``OpenAI`` LLM for the query engine.

    Inputs:
        temperature: Lower = more deterministic (0.0 is typical for Q&A).
        max_tokens: Cap on generated answer length.

    Returns:
        Configured ``OpenAI`` LLM instance.

    OpenAI:
        The client is created here; API calls happen when ``query_engine.query``
        runs.
    """
    require_openai_key()
    llm = OpenAI(
        model=config.OPENAI_LLM_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=config.OPENAI_API_KEY,
    )
    logger.info("Created OpenAI LLM model: %s", config.OPENAI_LLM_MODEL)
    return llm


def change_llm_model(new_model_id: str) -> None:
    """Switch the LLM model name in runtime config.

    What it does:
        Updates ``config.OPENAI_LLM_MODEL`` so the next ``create_openai_llm``
        call uses a different model.

    Inputs:
        new_model_id: OpenAI model id string (for example ``gpt-4o-mini``).

    Returns:
        None.

    OpenAI:
        No — only changes configuration.
    """
    config.OPENAI_LLM_MODEL = new_model_id
    logger.info("Changed LLM model to: %s", new_model_id)


# Coursera/watsonx vocabulary — same RAG architecture, different provider.
create_watsonx_embedding = create_openai_embedding
create_watsonx_llm = create_openai_llm