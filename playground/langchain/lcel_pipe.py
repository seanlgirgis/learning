"""Plug prompt, model, and parser into an LCEL chain.

Usage:

    from langchain_core.prompts import PromptTemplate
    from lcel_pipe import build_chain, str_chain
    from watson_llm import make_watsonx_chat

    prompt = PromptTemplate.from_template("Topic: {topic}\\nExplain briefly.")
    model = make_watsonx_chat()
    chain = str_chain(prompt, model)
    print(chain.invoke({"topic": "LCEL"}))
"""

from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableSerializable


def build_chain(
    prompt: Runnable,
    model: Runnable,
    parser: Runnable | None = None,
) -> RunnableSerializable:
    """Wire LCEL steps: prompt | model [| parser].

    Pass any LangChain Runnable for each slot — swap one piece without
    rewriting the rest of the pipeline.
    """
    if parser is None:
        return prompt | model
    return prompt | model | parser


def str_chain(prompt: Runnable, model: Runnable) -> RunnableSerializable:
    """Common pattern: prompt | model | StrOutputParser()."""
    return build_chain(prompt, model, StrOutputParser())