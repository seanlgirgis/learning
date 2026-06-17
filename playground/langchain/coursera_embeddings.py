"""WatsonxEmbeddings helper — reads WATSONX_* env (notebook twin).

Run set_env.ps1 before use.
"""

from __future__ import annotations

import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="ibm_watsonx_ai")

from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from langchain_ibm import WatsonxEmbeddings

DEFAULT_EMBED_MODEL = os.environ.get(
    "WATSONX_EMBEDDING_MODEL_ID",
    "ibm/slate-125m-english-rtrvr-v2",
)

default_embed_params = {
    EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
    EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
}


def make_embeddings(params: dict | None = None) -> WatsonxEmbeddings:
    """Build WatsonxEmbeddings from WATSONX_URL, PROJECT_ID, APIKEY."""
    return WatsonxEmbeddings(
        model_id=DEFAULT_EMBED_MODEL,
        url=os.environ["WATSONX_URL"],
        project_id=os.environ["WATSONX_PROJECT_ID"],
        apikey=os.environ["WATSONX_APIKEY"],
        params=params or default_embed_params,
    )