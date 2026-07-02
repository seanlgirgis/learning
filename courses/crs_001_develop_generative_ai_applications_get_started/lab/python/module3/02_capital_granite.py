"""Module 3 lab — first watsonx call (bite 1).

Run: python 02_capital_granite.py
If blank: python 02b_capital_debug.py
"""

from __future__ import annotations

import os
import sys

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

url = os.getenv("WATSONX_URL") or os.getenv("WATSONX_API_URL") or "https://us-south.ml.cloud.ibm.com"
api_key = os.environ.get("WATSONX_APIKEY") or os.environ.get("WATSONX_API_KEY")
project_id = os.environ.get("WATSONX_PROJECT_ID")

if not api_key or not project_id:
    print("Missing WATSONX_APIKEY or WATSONX_PROJECT_ID")
    sys.exit(1)

credentials = Credentials(url=url, api_key=api_key)
params = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 100,
}

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    params=params,
    credentials=credentials,
    project_id=project_id,
)

prompt = "Only reply with the answer. What is the capital of Canada?"
result = model.generate(prompt)
text = result["results"][0]["generated_text"]
print(text.strip() or "(empty — run 02b_capital_debug.py)")