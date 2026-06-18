"""IBM watsonx ModelInference from WATSONX_* env — playground lab helper.

Route A (IBM SDK): ModelInference from WATSONX_* env — used by .py labs and notebooks.

Run set_env.ps1 before importing:

    from watson_helper import model, model_id, credentials, parameters, project_id

    msg = model.generate("In today's sales meeting, we ")
    print(msg["results"][0]["generated_text"])

For LangChain pipes use watson_llm.make_watsonx_llm() instead.
"""

from __future__ import annotations

import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="ibm_watsonx_ai")

from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

REQUIRED_ENV = (
    "WATSONX_MODEL_ID",
    "WATSONX_URL",
    "WATSONX_PROJECT_ID",
    "WATSONX_APIKEY",
)

DEFAULT_PARAMETERS: dict = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.2,
}


def missing_watsonx_env() -> list[str]:
    """Names of required WATSONX_* variables that are not set."""
    return [name for name in REQUIRED_ENV if not os.getenv(name)]


def get_credentials() -> dict[str, str]:
    return {
        "url": os.environ["WATSONX_URL"],
        "api_key": os.environ["WATSONX_APIKEY"],
    }


def make_model_inference(params: dict | None = None) -> ModelInference:
    """Build ModelInference from WATSONX_* env."""
    merged = dict(DEFAULT_PARAMETERS)
    if params:
        merged.update(params)

    return ModelInference(
        model_id=os.environ["WATSONX_MODEL_ID"],
        params=merged,
        credentials=get_credentials(),
        project_id=os.environ["WATSONX_PROJECT_ID"],
    )


# Module-level defaults — import and use (notebook-style plug-in).
model_id = os.environ.get("WATSONX_MODEL_ID", "")
credentials = get_credentials() if not missing_watsonx_env() else {"url": "", "api_key": ""}
project_id = os.environ.get("WATSONX_PROJECT_ID", "")
parameters = dict(DEFAULT_PARAMETERS)
model = make_model_inference() if not missing_watsonx_env() else None