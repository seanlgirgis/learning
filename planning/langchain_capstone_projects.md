# LangChain Capstone Projects — Practice Plan

**Goal:** You write the code (bite by bite). Grok coaches, reviews traps, does not ghost-write whole files.

**Prerequisite:** Reference modules [01–19](../reference/langchain/index.html) + playground labs 08–35.

**How we work:** One capstone at a time → guide `capstone/capstone01.md` (etc.) + script in `playground/langchain/capstone/` → you fill bites → run → recall drill. Index: [capstones.md](../playground/langchain/capstone/capstones.md).

---

## Coverage matrix (what each capstone must touch)

| Module band | Ideas |
|-------------|--------|
| 01–04 | PromptTemplate, pipe, StrOutputParser |
| 05 | RunnableLambda (optional cap) |
| 06–07 | watson_helper vs watson_llm (at least Route B; A optional) |
| 08–10 | Chat messages OR ChatPromptTemplate in pipe |
| 09 | GenParams — new LLM per behavior |
| 11 | JsonOutputParser OR comma list — structured output |
| 12–16 | Load → split → embed → Chroma → retriever → answer |
| 17 | Conversation memory |
| 18 | Multi-step chain (LCEL assign or SequentialChain) |
| 19 | Agent + at least 2 tools |

---

## Capstone 1 — **Course Notes RAG Tutor** (RAG core)

**Story:** Two scripts — **ingest once**, **chat many times** (real-world pattern).

| Script | Job |
|--------|-----|
| `capstone_01_ingest.py` | **Consume** PDF (path or URL) → chunk → embed → **append Chroma**; dedupe via `ingest_manifest.json` |
| `capstone_01_chat.py` | Load saved Chroma → RetrievalQA → user questions (CLI or REPL) |

**Corpus:** `capstone/corpus_sources.json` — tiered RAG PDFs; `python capstone_01_ingest.py --corpus`

**Guide:** [capstone01.md](../playground/langchain/capstone/capstone01.md)

**Modules hit:** 07, 12–16 · recipes: Q&A pattern

---

## Capstone 2 — **Structured Review Desk** (pipe + JSON + multi-step)

**Story:** Paste a customer review → sentiment label → short summary → suggested reply (Exercise 6 twin, but yours).

**You build:**
1. Three `PromptTemplate`s (01)
2. LCEL with `RunnablePassthrough.assign` OR `SequentialChain` (18, 03)
3. Last step optional: `JsonOutputParser` for reply `{tone, response}` (11)
4. `make_watsonx_llm({GenParams.TEMPERATURE: 0.2})` (09)

**Stretch:** Batch mode — read reviews from a `.txt` file (05 lambda to truncate).

**Modules hit:** 01, 03, 04, 05, 09, 11, 18

---

## Capstone 3 — **Remember-Me Chat** (memory + chat template)

**Story:** REPL chat that remembers your name, preferences, and prior turns.

**You build:**
1. `ChatPromptTemplate` + system rules (10)
2. `ConversationBufferMemory` + `ConversationChain` (17)
3. `make_watsonx_llm` (07)
4. `input()` loop until `quit`

**Stretch:** Swap to `ConversationSummaryMemory` after 10 turns (Lab 33 bite 11).

**Modules hit:** 07, 08, 09, 10, 17 · recipe: chat-loop spirit

---

## Capstone 4 — **Research Agent** (agent + RAG tool)

**Story:** Agent with two tools: (1) calculator or Python REPL, (2) RAG over a small doc store you built in Capstone 1.

**You build:**
1. Reuse Chroma retriever as `@tool` that returns top chunk text (16, 19)
2. Second tool: `format_text` or calculator (35 Exercise 7)
3. `create_react_agent` + `AgentExecutor` (19)
4. Compare: same question via fixed RAG chain vs agent — when does agent win?

**Modules hit:** 07, 16, 19 (+ reuse 12–15 from capstone 1)

---

## Capstone 5 — **Full Stack Mini** (optional graduation)

**Story:** One script that offers modes: `rag`, `chat`, `review`, `agent` — subcommands.

**You build:** Compose capstones 1–4 behind `argparse` subcommands. Shared `watson_llm` setup only.

**Modules hit:** All 01–19

---

## Suggested order

1. **Capstone 1** — RAG (most new material in 12–16)
2. **Capstone 3** — Memory (smaller, confidence boost)
3. **Capstone 2** — Structured chains (18 + 11)
4. **Capstone 4** — Agent (needs RAG tool from 1)
5. **Capstone 5** — Optional glue

---

## Session rules (Sean)

- One bite per message when coding live
- Reference closed during rebuild drills
- Log traps you hit → `courses/crs_001/.../docs/TRAINING_LOG.md`

---

## Next step

Say **ingest bite 1** when ready — [capstone01.md](../playground/langchain/capstone/capstone01.md) → `capstone_01_ingest.py`, then `capstone_01_chat.py`.