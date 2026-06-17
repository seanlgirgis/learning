"""LCEL example — plug in prompt, model, and parser from shared helpers."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from lcel_pipe import build_chain, str_chain
from watson_llm import GenParams, make_watsonx_chat, make_watsonx_llm


def text_llm_pipe():
    """WatsonxLLM (plain text API) — same style as 02_watson_llm."""
    prompt = PromptTemplate.from_template(
        "Topic: {topic}\n"
        "Explain it to a beginner in one short sentence."
    )
    llm = make_watsonx_llm(
        params={
            GenParams.MAX_NEW_TOKENS: 80,
            GenParams.TEMPERATURE: 0.3,
        }
    )
    chain = str_chain(prompt, llm)
    return chain.invoke({"topic": "LCEL"})


def chat_model_pipe():
    """ChatWatsonx — matches course lab 05c_lcel_watsonx_pipeline."""
    prompt = PromptTemplate.from_template(
        "Topic: {topic}\n"
        "Explain it to a beginner in one short sentence "
        "of no more than 20 words."
    )
    model = make_watsonx_chat()
    chain = build_chain(prompt, model, StrOutputParser())
    return chain.invoke({"topic": "LCEL"})


if __name__ == "__main__":
    print("TEXT LLM PIPE (WatsonxLLM)")
    print("-" * 40)
    print(text_llm_pipe())

    print("\nCHAT MODEL PIPE (ChatWatsonx)")
    print("-" * 40)
    print(chat_model_pipe())