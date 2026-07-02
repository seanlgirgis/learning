"""Lab model layer — three ChatWatsonx models + per-model templates + JSON parser."""

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ibm import ChatWatsonx
from pydantic import BaseModel, Field

from config import (
    GRANITE_MODEL_ID,
    LLAMA_MODEL_ID,
    MISTRAL_MODEL_ID,
    PARAMETERS,
)

WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
PROJECT_ID = "skills-network"


class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(
        description="Sentiment score from 0 (negative) to 10 (positive)"
    )
    response: str = Field(description="Suggested response to the user")


json_parser = JsonOutputParser(pydantic_object=AIResponse)
FORMAT_PROMPT = json_parser.get_format_instructions()


def initialize_model(model_id: str) -> ChatWatsonx:
    return ChatWatsonx(
        model_id=model_id,
        url=WATSONX_URL,
        project_id=PROJECT_ID,
        params=PARAMETERS,
    )


llama_llm = initialize_model(LLAMA_MODEL_ID)
granite_llm = initialize_model(GRANITE_MODEL_ID)
mistral_llm = initialize_model(MISTRAL_MODEL_ID)

llama_template = PromptTemplate(
    template=(
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        "{system_prompt}\n{format_prompt}<|eot_id|>"
        "<|start_header_id|>user<|end_header_id|>\n"
        "{user_prompt}<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>\n"
    ),
    input_variables=["system_prompt", "format_prompt", "user_prompt"],
)

granite_template = PromptTemplate(
    template=(
        "<|system|>{system_prompt}\n{format_prompt}\n"
        "<|user|>{user_prompt}\n<|assistant|>"
    ),
    input_variables=["system_prompt", "format_prompt", "user_prompt"],
)

mistral_template = PromptTemplate(
    template="<s>[INST]{system_prompt}\n{format_prompt}\n{user_prompt}[/INST]",
    input_variables=["system_prompt", "format_prompt", "user_prompt"],
)


def get_ai_response(model, template, system_prompt: str, user_prompt: str) -> dict:
    chain = template | model | json_parser
    return chain.invoke(
        {
            "system_prompt": system_prompt,
            "format_prompt": FORMAT_PROMPT,
            "user_prompt": user_prompt,
        }
    )


def llama_response(system_prompt: str, user_prompt: str) -> dict:
    return get_ai_response(llama_llm, llama_template, system_prompt, user_prompt)


def granite_response(system_prompt: str, user_prompt: str) -> dict:
    return get_ai_response(granite_llm, granite_template, system_prompt, user_prompt)


def mistral_response(system_prompt: str, user_prompt: str) -> dict:
    return get_ai_response(mistral_llm, mistral_template, system_prompt, user_prompt)