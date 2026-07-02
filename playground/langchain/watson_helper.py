"""Playground lab helper — watsonx-compatible names, OpenAI backend.

Lab 15 and notebooks import ``model``, ``model_id``, ``credentials`` and call
``model.generate(prompt)`` like IBM ``ModelInference``. Implementation is OpenAI
via ``watson_llm.make_watsonx_llm`` (same stealth swap as the LangChain helper).

For LCEL pipes use ``watson_llm.make_watsonx_llm()`` instead.
"""

from __future__ import annotations

import os

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

from watson_llm import _openai_model, _to_text, make_watsonx_llm, missing_openai_env

DEFAULT_PARAMETERS: dict = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.2,
}


class _OpenAIModelInferenceShim:
    """Mimics ``ModelInference.generate()`` return shape for Lab 15."""

    def __init__(self, params: dict | None = None) -> None:
        self._llm = make_watsonx_llm(params)

    def generate(self, prompt, **kwargs):
        if isinstance(prompt, list):
            prompt = prompt[0]
        text = _to_text(self._llm.invoke(prompt))
        return {"results": [{"generated_text": text}]}


def missing_watsonx_env() -> list[str]:
    return missing_openai_env()


def get_credentials() -> dict[str, str]:
    return {
        "url": "https://api.openai.com/v1",
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
    }


def make_model_inference(params: dict | None = None) -> _OpenAIModelInferenceShim:
    merged = dict(DEFAULT_PARAMETERS)
    if params:
        merged.update(params)
    return _OpenAIModelInferenceShim(merged)


# Module-level defaults — notebook-style plug-in (Lab 15).
model_id = _openai_model()
credentials = get_credentials()
project_id = "openai"
parameters = dict(DEFAULT_PARAMETERS)
model = make_model_inference() if not missing_openai_env() else None