# Capstone code patterns — RemNote deck

Import after `12-module3-lab-quiz.md`. Maps playground capstones to course ideas.

---

## Capstone 01 — RAG

- Capstone 01 ingest pipeline order? >>A)
    - Load documents → split → embed → store in Chroma
    - Chat → retrieve → embed → split
    - Flask → Chroma → ingest
    - Agent → tool → Chroma only at query time without ingest

- Capstone 01 chat uses retrieval for? >>A)
    - Grounding answers in course PDF chunks before LLM generates
    - Storing Flask session IDs
    - Fine-tuning model weights
    - Replacing PromptTemplate with JsonOutputParser only

- Chroma collection for current OpenAI ingest in capstone 01? >>A)
    - `chroma_01_openai` (re-ingest with `--corpus --force` if missing)
    - `chroma_01` only without re-embed
    - Redis
    - `templates/`

---

## Capstone 02 — Review desk

- Review desk pattern is? >>A)
    - Fixed multi-step chain (sentiment → summary → reply) — not an agent
    - ReAct agent with calculator
    - RAG-only with no LLM
    - RunnableParallel only

---

## Capstone 03 — Memory

- Remember-me chat separates users by? >>A)
    - `session_id` key → load/save message history for that key
    - Model name in Flask only
    - Random prompt each turn
    - Global variable shared by all users

---

## Capstone 04 — Agent

- Capstone 04 router is? >>A)
    - ReAct agent — LLM chooses tools from descriptions each turn
    - Fixed RAG chain on every question
    - Flask `/generate` only
    - RunnableParallel sentiment + summary

- Agent LLM in capstone 04 should use? >>A)
    - `make_watsonx_agent_llm()` (ReAct / stop compatibility)
    - Raw `ModelInference.generate` only
    - `granite_response` from Module 3 lab unchanged
    - No LLM — tools only

- `search_course_docs` tool wraps? >>A)
    - RAG retrieval over ingested course docs (capstone 01 corpus)
    - Wikipedia API only
    - Flask session store
    - JsonOutputParser

---

## Capstone vs course lab

- Module 3 `model.py` vs Capstone 04 agent? >>A)
    - Lab: you pick model per request, fixed chain; Capstone 4: LLM picks tools
    - Both are identical ReAct agents
    - Lab uses agents; capstone uses only raw HTTP
    - Neither uses LangChain