"""RAG question-answering: retrieve chunks, augment prompt, call LLM.

Mental model — query engine:
    1. Embed the user's question
    2. Retriever finds the most relevant chunks (top-k from the index)
    3. Prompt template inserts chunks into ``{context_str}``
    4. LLM writes the final answer

This is not a direct ``llm.invoke(question)`` call. The query engine runs the
full retrieve-then-generate pipeline for you.

Coursera used watsonx for step 4; this lab uses OpenAI. Steps 1–3 are the same.
"""

import logging
from typing import Any

from llama_index.core import PromptTemplate, VectorStoreIndex

import config
from modules.llm_interface import create_openai_llm

logger = logging.getLogger(__name__)


def generate_initial_facts(index: VectorStoreIndex) -> str:
    """Generate three icebreaker facts from the indexed profile.

    What it does:
        Runs a query engine with ``INITIAL_FACTS_TEMPLATE`` to produce three
        career/education facts grounded in retrieved profile chunks.

    Inputs:
        index: Built ``VectorStoreIndex`` (searchable memory).

    Returns:
        Answer string from the LLM, or an error message string on failure.

    OpenAI:
        Yes — retrieval uses embeddings; answer uses the LLM.
    """
    try:
        llm = create_openai_llm(temperature=0.0, max_tokens=500)
        facts_prompt = PromptTemplate(template=config.INITIAL_FACTS_TEMPLATE)
        # Query engine = retriever + prompt augmentation + LLM in one object.
        query_engine = index.as_query_engine(
            streaming=False,
            similarity_top_k=config.SIMILARITY_TOP_K,
            llm=llm,
            text_qa_template=facts_prompt,
        )
        query = (
            "Provide three interesting facts about this person's career, "
            "education, or professional background."
        )
        response = query_engine.query(query)
        return response.response
    except Exception as exc:
        logger.error("Error in generate_initial_facts: %s", exc)
        return "Failed to generate initial facts."


def answer_user_query(index: VectorStoreIndex, user_query: str) -> Any:
    """Answer a follow-up question about the profile using RAG.

    What it does:
        Retrieves relevant chunks, fills ``USER_QUESTION_TEMPLATE``, and calls
        the LLM to produce a grounded answer.

    Inputs:
        index: Built ``VectorStoreIndex``.
        user_query: Natural-language question from the user.

    Returns:
        LlamaIndex response object (use ``.response`` for the answer text), or
        an error string on failure.

    OpenAI:
        Yes — retrieval uses embeddings; answer uses the LLM.
    """
    try:
        llm = create_openai_llm(temperature=0.0, max_tokens=250)
        question_prompt = PromptTemplate(template=config.USER_QUESTION_TEMPLATE)
        query_engine = index.as_query_engine(
            streaming=False,
            similarity_top_k=config.SIMILARITY_TOP_K,
            llm=llm,
            text_qa_template=question_prompt,
        )
        return query_engine.query(user_query)
    except Exception as exc:
        logger.error("Error in answer_user_query: %s", exc)
        return "Failed to get an answer."