"""
Tutor review Example 3 — few-shot (examples inside the prompt).

Concepts:
  - few-shot = 2+ worked examples in the prompt (still runtime, not fine-tune)
  - example_prompt = how ONE example is formatted
  - examples = list of dicts (the sample rows)
  - prefix / suffix = intro + the real question with blanks
  - FewShotPromptTemplate stitches them into one big string

This file: fill-only demo first, then optional real LLM classify.
Needs set_env.ps1; LLM part needs OPENAI_API_KEY.
"""

import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

# How each example row looks when written into the prompt
promptExample = PromptTemplate.from_template(
    "Text: {text}\nCategory: {category}"
)

# Two (or more) worked examples → few-shot
examples = [
    {"text": "I was charged twice.", "category": "billing"},
    {"text": "The application will not start.", "category": "technical"},
]

# BUILD few-shot recipe
prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=promptExample,
    prefix="Classify the support request using the examples.",
    suffix="Text: {request}\nCategory:",
    input_variables=["request"],
)

# A) FILL only — see the full prompt string (examples + new request)
filled = prompt.invoke({"request": "My invoice has the wrong amount."})
print("=== A) few-shot prompt.invoke → fill only ===")
print(filled.to_string())
print()

# B) Real LLM call — model should continue the pattern (e.g. billing)
model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-5.4-nano"))
chain = prompt | model | StrOutputParser()
answer = chain.invoke({"request": "My invoice has the wrong amount."})
print("=== B) chain.invoke → few-shot + LLM ===")
print(answer)
