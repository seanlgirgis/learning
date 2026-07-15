"""
Tutor review Example 2 — ChatPromptTemplate (roles + messages).

Concepts:
  - from_messages  → BUILD a chat recipe (list of role turns)
  - ("system", ...) / ("human", ...)  → roles (LangChain words)
  - invoke({...})  → FILL blanks in those messages
  - .messages      → the prepared message list (still no LLM)

Vocabulary trap:
  everyday "user"  → LangChain template role "human"
  everyday "assistant" → LangChain template role "ai"

No API key needed. Run after set_env.ps1.
"""

from langchain_core.prompts import ChatPromptTemplate

# ---------------------------------------------------------------------------
# 1) BUILD — list of (role, content) pairs
#    Method name to remember: from_messages  (NOT from_template, NOT invoke)
# ---------------------------------------------------------------------------
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a concise tutor. Answer in one short sentence."),
        ("human", "{question}"),
    ]
)

# ---------------------------------------------------------------------------
# 2) FILL — keys match {blanks}; still no LLM call
# ---------------------------------------------------------------------------
result = chat_prompt.invoke({"question": "What is RAG?"})

# ---------------------------------------------------------------------------
# 3) READ — chat templates produce a message LIST on .messages
# ---------------------------------------------------------------------------
print("--- prepared messages ---")
for msg in result.messages:
    # msg.type is often "system" / "human"; content is the text
    print(f"{msg.type}: {msg.content}")

# Expected idea:
# system: You are a concise tutor. Answer in one short sentence.
# human: What is RAG?

# ---------------------------------------------------------------------------
# 4) Same chat recipe, different question
# ---------------------------------------------------------------------------
result2 = chat_prompt.invoke({"question": "What is a vector database?"})
print("--- second fill ---")
for msg in result2.messages:
    print(f"{msg.type}: {msg.content}")
