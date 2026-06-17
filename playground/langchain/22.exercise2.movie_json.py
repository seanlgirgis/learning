"""Lab 22 — Exercise 2: movie JSON (notebook twin).

Bare JsonOutputParser() + hand-written format instructions (no Pydantic class).

Run set_env.ps1, then:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\22.exercise2.movie_json.py
"""

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from langchain_helper import make_llm

json_parser = JsonOutputParser()

format_instructions = """RESPONSE FORMAT: Return ONLY a single JSON object—no markdown, no examples, no extra keys.  It must look exactly like:
{
  "title": "movie title",
  "director": "director name",
  "year": 2000,
  "genre": "movie genre"
}

IMPORTANT: Your response must be *only* that JSON.  Do NOT include any illustrative or example JSON."""

prompt_template = PromptTemplate(
    template="""You are a JSON-only assistant.

Task: Generate info about the movie "{movie_name}" in JSON format.

{format_instructions}
""",
    input_variables=["movie_name"],
    partial_variables={"format_instructions": format_instructions},
)

movie_chain = prompt_template | make_llm() | json_parser

movie_name = "The Matrix"
result = movie_chain.invoke({"movie_name": movie_name})

print("Parsed result:")
print(f"Title: {result['title']}")
print(f"Director: {result['director']}")
print(f"Year: {result['year']}")
print(f"Genre: {result['genre']}")