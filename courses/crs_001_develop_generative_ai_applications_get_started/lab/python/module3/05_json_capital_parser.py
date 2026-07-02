"""Bite 4 — JsonOutputParser (structured dict, not plain text).

Run:
    pip install pydantic   # usually already installed with langchain
    python 05_json_capital_parser.py
"""

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ibm import ChatWatsonx
from pydantic import BaseModel, Field

WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
PROJECT_ID = "skills-network"


class CapitalAnswer(BaseModel):
    """Lab-style structured response."""

    country: str = Field(description="The country asked about")
    capital: str = Field(description="The capital city name only")


parser = JsonOutputParser(pydantic_object=CapitalAnswer)

prompt = PromptTemplate(
    template=(
        "Answer the geography question.\n"
        "Question: {question}\n\n"
        "{format_instructions}\n"
        "Return only valid JSON."
    ),
    input_variables=["question"],
    partial_variables={
        "format_instructions": parser.get_format_instructions(),
    },
)

llm = ChatWatsonx(
    model_id="ibm/granite-4-h-small",
    url=WATSONX_URL,
    project_id=PROJECT_ID,
    params={"max_new_tokens": 150},
)

chain = prompt | llm | parser

result = chain.invoke({"question": "What is the capital of Canada?"})

print(type(result).__name__, result)
print("capital field:", result.get("capital", "(missing)"))