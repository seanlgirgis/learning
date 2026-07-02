"""Bite 1 fix B — Granite chat tokens + lab-style auth (no api_key in Credentials)."""

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

credentials = Credentials(url="https://us-south.ml.cloud.ibm.com")

params = {
    GenParams.MAX_NEW_TOKENS: 100,
}

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    params=params,
    credentials=credentials,
    project_id="skills-network",
)

prompt = (
    "<|system|>Reply with only the answer, nothing else.\n"
    "<|user|>What is the capital of Canada?\n"
    "<|assistant|>"
)

result = model.generate(prompt)
text = result["results"][0]["generated_text"]
print(repr(text))
print(text.strip() or "(still empty)")