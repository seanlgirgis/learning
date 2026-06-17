"""WatsonxLLM helpers for local Coursera notebook copies.

All connection settings come from WATSONX_* env vars (set_env.ps1).
"""

from __future__ import annotations

import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="ibm_watsonx_ai")

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_ibm import WatsonxLLM

DEFAULT_PARAMS: dict = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.MIN_NEW_TOKENS: 0,
    GenParams.TEMPERATURE: 0.5,
    GenParams.TOP_P: 0.2,
    GenParams.TOP_K: 1,
}


def make_llm(params: dict | None = None) -> WatsonxLLM:
    """Build WatsonxLLM using WATSONX_MODEL_ID, URL, PROJECT_ID, APIKEY from env."""
    merged = dict(DEFAULT_PARAMS)
    if params:
        merged.update(params)

    return WatsonxLLM(
        model_id=os.environ["WATSONX_MODEL_ID"],
        url=os.environ["WATSONX_URL"],
        project_id=os.environ["WATSONX_PROJECT_ID"],
        apikey=os.environ["WATSONX_APIKEY"],
        params=merged,
    )


def llm_model(prompt_txt: str, params: dict | None = None) -> str:
    """Same signature as the Coursera In-Context lab — uses your env vars."""
    return make_llm(params).invoke(prompt_txt)