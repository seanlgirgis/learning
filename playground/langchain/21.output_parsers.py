"""Lab 21 — output parsers: JSON (Joke) and comma-separated list.

Part A: JsonOutputParser + Pydantic Joke -> dict
Part B: CommaSeparatedListOutputParser -> list
Exercise 2 (movie JSON) is Lab 22.

Run set_env.ps1, then:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\21.output_parsers.py
"""

from langchain_classic.output_parsers import CommaSeparatedListOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

from watson_llm import make_watsonx_llm


class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")


# --- Part A: JSON joke ---

joke_parser = JsonOutputParser(pydantic_object=Joke)
joke_format = joke_parser.get_format_instructions()

joke_prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": joke_format},
)

joke_chain = joke_prompt | make_watsonx_llm() | joke_parser
print("Part A — joke:")
print(joke_chain.invoke({"query": "Tell me a joke."}))
print()

# --- Part B: comma-separated list ---

list_parser = CommaSeparatedListOutputParser()
list_format = list_parser.get_format_instructions()

list_prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\nList five {subject}.",
    input_variables=["subject"],
    partial_variables={"format_instructions": list_format},
)

list_chain = list_prompt | make_watsonx_llm() | list_parser
print("Part B — languages:")
print(list_chain.invoke({"subject": "programming languages"}))