"""
Tutor review Example 1b — PromptTemplate + real LLM call.

Builds on 01_prompt_template_fill.py:
  - Step A: prompt.invoke  → FILL blanks only (no model)
  - Step B: chain.invoke   → FILL + CALL the LLM (real API)

Needs:
  - set_env.ps1 (venv)
  - OPENAI_API_KEY in the environment (same as your other OpenAI labs)

Optional:
  - OPENAI_MODEL  (default: gpt-5.4-nano, matches crs_001 lab 05b)
"""

import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# ---------------------------------------------------------------------------
# 0) Model — this object can call OpenAI
# ---------------------------------------------------------------------------
model_name = os.getenv("OPENAI_MODEL", "gpt-5.4-nano")
model = ChatOpenAI(model=model_name)

# ---------------------------------------------------------------------------
# 1) BUILD recipe — same idea as Example 1
# ---------------------------------------------------------------------------
prompt = PromptTemplate.from_template(
    "Explain {topic} in one short sentence for a beginner."
)

# ---------------------------------------------------------------------------
# 2) FILL only — still NO LLM (same as file 01)
# ---------------------------------------------------------------------------
filled = prompt.invoke({"topic": "RAG"})
print("=== A) prompt.invoke  → fill only (no LLM) ===")
print(filled.to_string())
print()

# ---------------------------------------------------------------------------
# 3) Pipe: prompt | model | parser
#    LCEL "|" means: take output of left, feed as input to right
# ---------------------------------------------------------------------------
chain = prompt | model | StrOutputParser()

# ---------------------------------------------------------------------------
# 4) FILL + CALL LLM — this is the real network/model call
#    chain.invoke uses the same {topic} dict as prompt.invoke
# ---------------------------------------------------------------------------
answer = chain.invoke({"topic": "RAG"})
print("=== B) chain.invoke  → fill + LLM call ===")
print(answer)
print()

# ---------------------------------------------------------------------------
# 5) Same chain, different blank value
# ---------------------------------------------------------------------------
answer2 = chain.invoke({"topic": "vector databases"})
print("=== B again, different topic ===")
print(answer2)

# Recall anchors:
#   prompt.invoke  = prepare text
#   model.invoke   = call LLM once (with messages/text already prepared)
#   chain.invoke   = run the whole pipe (prepare → model → parse string)
