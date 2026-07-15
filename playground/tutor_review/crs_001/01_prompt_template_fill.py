"""
Tutor review Example 1 — PromptTemplate (string recipe).

Concepts:
  - from_template  → BUILD the recipe (create the template)
  - {topic}        → a blank you fill later
  - invoke({...})  → FILL the blanks (still no LLM call)
  - to_string()    → the final plain text after filling

No API key needed. Run after set_env.ps1.
"""

from langchain_core.prompts import PromptTemplate

# ---------------------------------------------------------------------------
# 1) BUILD — create a reusable string recipe with a blank: {topic}
#    Method name to remember: from_template
# ---------------------------------------------------------------------------
prompt = PromptTemplate.from_template(
    "Explain {topic} in one sentence."
)

# ---------------------------------------------------------------------------
# 2) FILL — pass a dict; keys must match the {blank} names in the template
#    Method name to remember: invoke
#    This does NOT call an LLM. It only fills the blanks.
# ---------------------------------------------------------------------------
result = prompt.invoke({"topic": "RAG"})

# ---------------------------------------------------------------------------
# 3) READ — turn the prepared prompt into a plain string for display
# ---------------------------------------------------------------------------
print("--- filled prompt ---")
print(result.to_string())
# Expected:
# Explain RAG in one sentence.

# ---------------------------------------------------------------------------
# 4) Same recipe, different value — that's why templates exist
# ---------------------------------------------------------------------------
result2 = prompt.invoke({"topic": "vector databases"})
print("--- second fill ---")
print(result2.to_string())
# Expected:
# Explain vector databases in one sentence.
