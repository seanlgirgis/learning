"""ModelInference setup for the LangChain Coursera lab (local env)."""

from __future__ import annotations

import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="ibm_watsonx_ai")

from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

model_id = os.environ["WATSONX_MODEL_ID"]

credentials = {
    "url": os.environ["WATSONX_URL"],
    "api_key": os.environ["WATSONX_APIKEY"],
}

parameters = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.2,
}

project_id = os.environ["WATSONX_PROJECT_ID"]

model = ModelInference(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=project_id,
)