"""Playground provider helper — watsonx-compatible names, OpenAI backend.

Course labs still import ``make_watsonx_llm``, ``make_watsonx_embeddings``, and
``GenParams``; all traffic goes to OpenAI via ``OPENAI_API_KEY`` / ``OPENAI_MODEL``
(and ``OPENAI_EMBEDDING_MODEL`` for vectors). IBM watsonx is not called.

Swap rationale (2026): IBM learning tokens exhausted; capstones + ~35 playground
scripts should keep running without rewrites. Later: add Grok or flip env to
multi-provider.

Usage:

    from watson_llm import GenParams, llm_model, make_watsonx_embeddings, make_watsonx_llm

    llm = make_watsonx_llm()                    # LCEL, LLMChain, agents
    emb = make_watsonx_embeddings()            # Chroma / RAG (re-ingest after swap)
    text = llm_model("What is the capital of France?")
"""

from __future__ import annotations

import os
from typing import Any

from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import LanguageModelInput
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Re-export for labs that build param dicts (values map to OpenAI kwargs; IBM-only keys ignored).
__all__ = [
    "EmbedTextParamsMetaNames",
    "GenParams",
    "llm_model",
    "make_watsonx_agent_llm",
    "make_watsonx_chat",
    "make_watsonx_embeddings",
    "make_watsonx_llm",
    "missing_openai_env",
    "missing_watsonx_env",
]

REQUIRED_OPENAI_ENV = ("OPENAI_API_KEY",)

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_AGENT_MODEL = "gpt-4o-mini"
DEFAULT_OPENAI_EMBED_MODEL = "text-embedding-3-small"

DEFAULT_PARAMS: dict = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.MIN_NEW_TOKENS: 0,
    GenParams.TEMPERATURE: 0.5,
    GenParams.TOP_P: 0.2,
    GenParams.TOP_K: 1,
}


def _openai_model() -> str:
    return os.environ.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)


def _openai_embedding_model() -> str:
    return os.environ.get("OPENAI_EMBEDDING_MODEL", DEFAULT_OPENAI_EMBED_MODEL)


def _merge_params(params: dict | None) -> dict:
    merged = dict(DEFAULT_PARAMS)
    if params:
        merged.update(params)
    return merged


def _model_supports_stop_sequences(model: str) -> bool:
    """ReAct agents pass stop=; gpt-5.x reasoning models reject that parameter."""
    name = model.lower()
    if name.startswith(("gpt-4", "gpt-3")):
        return True
    if "chat" in name and name.startswith("gpt-5"):
        return True
    if name.startswith(("gpt-5", "o1", "o3", "o4")):
        return False
    return True


class AgentCompatibleChatOpenAI(ChatOpenAI):
    """ChatOpenAI that omits stop sequences when the model does not support them."""

    def _get_request_payload(
        self,
        input_: LanguageModelInput,
        *,
        stop: list[str] | None = None,
        **kwargs: Any,
    ) -> dict:
        if not _model_supports_stop_sequences(self.model_name):
            stop = None
        return super()._get_request_payload(input_, stop=stop, **kwargs)


def _openai_kwargs(params: dict | None) -> dict:
    """Map GenParams-style dicts to ChatOpenAI keyword args."""
    merged = _merge_params(params)
    kwargs: dict = {}

    temperature = merged.get(GenParams.TEMPERATURE, merged.get("temperature"))
    max_tokens = merged.get(GenParams.MAX_NEW_TOKENS, merged.get("max_new_tokens"))
    top_p = merged.get(GenParams.TOP_P, merged.get("top_p"))

    if temperature is not None:
        kwargs["temperature"] = temperature
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
    if top_p is not None:
        kwargs["top_p"] = top_p

    return kwargs


def _to_text(result) -> str:
    if isinstance(result, str):
        return result
    content = getattr(result, "content", None)
    if content is not None:
        return content
    return str(result)


def make_watsonx_llm(params: dict | None = None) -> BaseChatModel:
    """Chat LLM for LCEL, LLMChain, ConversationChain."""
    return AgentCompatibleChatOpenAI(model=_openai_model(), **_openai_kwargs(params))


def make_watsonx_agent_llm(params: dict | None = None) -> BaseChatModel:
    """LLM for ReAct / AgentExecutor — needs stop sequences (gpt-4o-mini fallback)."""
    model = _openai_model()
    if not _model_supports_stop_sequences(model):
        model = os.environ.get("OPENAI_AGENT_MODEL", DEFAULT_AGENT_MODEL)
    return AgentCompatibleChatOpenAI(model=model, **_openai_kwargs(params))


def make_watsonx_chat(params: dict | None = None) -> BaseChatModel:
    """Alias for ``make_watsonx_llm`` (course notebooks used both names)."""
    return make_watsonx_llm(params)


def make_watsonx_embeddings(params: dict | None = None) -> Embeddings:
    """Embeddings for Chroma / RAG labs (OpenAI; ``params`` kept for call-site compat)."""
    del params  # IBM TRUNCATE_INPUT_TOKENS etc. do not apply to OpenAI embeddings.
    return OpenAIEmbeddings(model=_openai_embedding_model())


def llm_model(prompt_txt: str, params: dict | None = None) -> str:
    """Single-shot text prompt → string reply."""
    return _to_text(make_watsonx_llm(params).invoke(prompt_txt))


def missing_openai_env() -> list[str]:
    """Return required OpenAI variables that are not set."""
    return [name for name in REQUIRED_OPENAI_ENV if not os.getenv(name)]


def missing_watsonx_env() -> list[str]:
    """Legacy name — delegates to ``missing_openai_env`` after provider swap."""
    return missing_openai_env()