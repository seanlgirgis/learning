"""Bite 2b — Llama with special tokens (lab fix).

Run after 03_capital_llama_plain.py:
    python 03_capital_llama_tokens.py
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

prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an expert assistant who provides concise and accurate answers.<|eot_id|>
<|start_header_id|>user<|end_header_id|>
What is the capital of Canada?<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

text = model.generate(prompt)["results"][0]["generated_text"]
print(text.strip())