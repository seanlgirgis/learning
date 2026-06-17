"""LangChain WatsonxLLM from WATSONX_* env — playground lab helper.

Notebook twin of playground/notebooks/coursera_llm_model.py.

Run set_env.ps1 before importing:

    from langchain_helper import make_llm

    llama_llm = make_llm()
    print(llama_llm.invoke("Who is man's best friend?"))

For IBM SDK model.generate() use watson_helper instead.
For the full API surface see watson_llm.py (make_watsonx_llm, ChatWatsonx, etc.).
"""

from __future__ import annotations

from watson_llm import (
    GenParams,
    llm_model,
    make_watsonx_llm,
    missing_watsonx_env,
)
from langchain_ibm import WatsonxLLM


def make_llm(params: dict | None = None) -> WatsonxLLM:
    """Build WatsonxLLM using WATSONX_MODEL_ID, URL, PROJECT_ID, APIKEY from env."""
    return make_watsonx_llm(params)


__all__ = [
    "GenParams",
    "llm_model",
    "make_llm",
    "make_watsonx_llm",
    "missing_watsonx_env",
]