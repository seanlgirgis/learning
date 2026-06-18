"""Reusable IBM watsonx text LLM helper for playground scripts.

Usage from any file in playground/langchain/:

    from watson_llm import GenParams, llm_model, make_watsonx_embeddings, make_watsonx_llm

    response = llm_model("What is the capital of France?")
    llm = make_watsonx_llm()  # plug into LCEL: prompt | llm | parser
    emb = make_watsonx_embeddings()  # RAG / Chroma labs

Run scripts from this folder (or add it to PYTHONPATH):

    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\02_watson_llm.py
"""

from __future__ import annotations

import os
import warnings

# IBM SDK warnings on every call — safe to hide while learning.
# (1) Mistral is a third-party model on watsonx — license notice.
# (2) WatsonxLLM uses legacy text/generation API; ChatWatsonx uses the newer chat API.
warnings.filterwarnings("ignore", category=UserWarning, module="ibm_watsonx_ai")

from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_ibm import ChatWatsonx, WatsonxEmbeddings, WatsonxLLM

REQUIRED_ENV = (
    "WATSONX_MODEL_ID",
    "WATSONX_URL",
    "WATSONX_PROJECT_ID",
    "WATSONX_APIKEY",
)

DEFAULT_PARAMS: dict = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.MIN_NEW_TOKENS: 0,
    GenParams.TEMPERATURE: 0.5,
    GenParams.TOP_P: 0.2,
    GenParams.TOP_K: 1,
}


def _watsonx_credentials() -> dict[str, str]:
    return {
        "model_id": os.environ["WATSONX_MODEL_ID"],
        "url": os.environ["WATSONX_URL"],
        "project_id": os.environ["WATSONX_PROJECT_ID"],
        "apikey": os.environ["WATSONX_APIKEY"],
    }


def _merge_params(params: dict | None) -> dict:
    merged = dict(DEFAULT_PARAMS)
    if params:
        merged.update(params)
    return merged


def make_watsonx_llm(params: dict | None = None) -> WatsonxLLM:
    """Build a WatsonxLLM object for LCEL or repeated invoke calls."""
    creds = _watsonx_credentials()
    return WatsonxLLM(
        model_id=creds["model_id"],
        url=creds["url"],
        project_id=creds["project_id"],
        apikey=creds["apikey"],
        params=_merge_params(params),
    )


def make_watsonx_chat(params: dict | None = None) -> ChatWatsonx:
    """Build a ChatWatsonx object — matches course LCEL chat pipelines."""
    creds = _watsonx_credentials()
    return ChatWatsonx(
        model_id=creds["model_id"],
        url=creds["url"],
        project_id=creds["project_id"],
        apikey=creds["apikey"],
        params=_merge_params(params),
    )


def llm_model(prompt_txt: str, params: dict | None = None) -> str:
    """Send a text prompt to IBM watsonx and return the model's reply.

    Reads connection settings from environment variables set by set_env.ps1:
    WATSONX_MODEL_ID, WATSONX_URL, WATSONX_PROJECT_ID, WATSONX_APIKEY.

    Args:
        prompt_txt: The prompt string sent to the model (plain text, not a dict).
        params: Optional dict of generation settings that override the defaults.
            Keys may use GenParams constants or plain strings (e.g. "temperature").
            Example: params={"temperature": 0.9} keeps other defaults unchanged.

    Returns:
        The model response as a string (from WatsonxLLM.invoke).

    Raises:
        KeyError: If a required WATSONX_* environment variable is missing.
    """
    return make_watsonx_llm(params).invoke(prompt_txt)


def missing_watsonx_env() -> list[str]:
    """Return names of required WATSONX_* variables that are not set."""
    return [name for name in REQUIRED_ENV if not os.getenv(name)]


DEFAULT_EMBED_MODEL = os.environ.get(
    "WATSONX_EMBEDDING_MODEL_ID",
    "ibm/slate-125m-english-rtrvr-v2",
)

DEFAULT_EMBED_PARAMS: dict = {
    EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
    EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
}


def make_watsonx_embeddings(params: dict | None = None) -> WatsonxEmbeddings:
    """Build WatsonxEmbeddings from WATSONX_URL, PROJECT_ID, APIKEY."""
    creds = _watsonx_credentials()
    return WatsonxEmbeddings(
        model_id=DEFAULT_EMBED_MODEL,
        url=creds["url"],
        project_id=creds["project_id"],
        apikey=creds["apikey"],
        params=params or DEFAULT_EMBED_PARAMS,
    )