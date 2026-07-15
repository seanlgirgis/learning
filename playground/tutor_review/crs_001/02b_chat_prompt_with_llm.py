"""
Tutor review Example 2b — ChatPromptTemplate + real LLM call.

Builds on 02_chat_prompt_template_fill.py:
  - from_messages → BUILD turns (system / human)
  - chain.invoke  → FILL blanks + CALL the model

Needs set_env.ps1 + OPENAI_API_KEY.
"""

import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model_name = os.getenv("OPENAI_MODEL", "gpt-5.4-nano")
model = ChatOpenAI(model=model_name)

# BUILD: turns with roles; blanks live in content
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a concise tutor. Answer in one short sentence."),
        ("human", "{question}"),
    ]
)

# Demo only: FILL turns, no LLM
filled = chat_prompt.invoke({"question": "What is RAG?"})
print("=== A) chat_prompt.invoke → fill turns only ===")
for msg in filled.messages:
    print(f"{msg.type}: {msg.content}")
print()

# Real path: turns → model → string
chain = chat_prompt | model | StrOutputParser()
answer = chain.invoke({"question": "What is RAG?"})
print("=== B) chain.invoke → fill turns + LLM ===")
print(answer)
print()

answer2 = chain.invoke({"question": "What is a vector database?"})
print("=== B again, different question ===")
print(answer2)
