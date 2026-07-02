"""Bite 2a — Llama without special tokens (lab shows messy output).

Run in Cloud IDE venv:
    python 03_capital_llama_plain.py
"""

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

credentials = Credentials(url="https://us-south.ml.cloud.ibm.com")

model = ModelInference(
    model_id="meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
    params={GenParams.MAX_NEW_TOKENS: 100},
    credentials=credentials,
    project_id="skills-network",
)

prompt = "Only reply with the answer. What is the capital of Canada?"
text = model.generate(prompt)["results"][0]["generated_text"]
print("--- raw ---")
print(repr(text))
print("--- stripped ---")
print(text.strip() or "(empty)")