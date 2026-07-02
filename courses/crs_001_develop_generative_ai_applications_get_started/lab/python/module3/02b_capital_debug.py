"""Bite 1 debug — why capital.py prints nothing."""

from __future__ import annotations

import json
import os
import sys
import traceback

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams


def mask(name: str) -> str:
    v = os.getenv(name)
    return "MISSING" if not v else f"set len={len(v)}"


def main() -> None:
    print("=== capital debug ===")
    print("python:", sys.version.split()[0])
    for key in ("WATSONX_URL", "WATSONX_APIKEY", "WATSONX_PROJECT_ID", "WATSONX_AI_AUTH_TYPE"):
        print(f"  {key}: {mask(key)}")

    url = os.getenv("WATSONX_URL") or os.getenv("WATSONX_API_URL") or "https://us-south.ml.cloud.ibm.com"
    api_key = os.environ.get("WATSONX_APIKEY") or os.environ.get("WATSONX_API_KEY")
    project_id = os.environ.get("WATSONX_PROJECT_ID")

    if not api_key or not project_id:
        print("STOP: missing WATSONX_APIKEY or WATSONX_PROJECT_ID")
        sys.exit(1)

    credentials = Credentials(url=url, api_key=api_key)
    params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: 100,
    }

    print("url:", url)
    print("model_id: ibm/granite-4-h-small")
    print("calling generate...")

    try:
        model = ModelInference(
            model_id="ibm/granite-4-h-small",
            params=params,
            credentials=credentials,
            project_id=project_id,
        )
        prompt = "Only reply with the answer. What is the capital of Canada?"
        raw = model.generate(prompt)
        print("--- raw response (first 1500 chars) ---")
        text = json.dumps(raw, indent=2, default=str)
        print(text[:1500])
        if len(text) > 1500:
            print("... truncated ...")

        results = raw.get("results") if isinstance(raw, dict) else None
        if not results:
            print("WARN: no 'results' key — check structure above")
            return
        gen = results[0].get("generated_text", "")
        print("--- generated_text repr ---")
        print(repr(gen))
        print("--- stripped ---")
        print(gen.strip() or "(empty after strip)")
    except Exception:
        print("ERROR:")
        traceback.print_exc()


if __name__ == "__main__":
    main()