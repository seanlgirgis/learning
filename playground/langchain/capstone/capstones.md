# Capstones — index

**What this folder is:** Your **practice apps** — not copy-paste labs. One `.py` per project. You type each bite; Grok coaches.

**Where:** `playground/langchain/capstone/`  
**Full plan:** [planning/langchain_capstone_projects.md](../../../planning/langchain_capstone_projects.md)

---

## Start here

| # | Guide | Script | Status |
|---|--------|--------|--------|
| **1** | **[capstone01.md](capstone01.md)** | `capstone_01_ingest.py` + `capstone_01_chat.py` | **Done** |
| **3** | **[capstone03.md](capstone03.md)** | `capstone_03_remember_me_chat.py` | **Done** |
| **2** | **[capstone02.md](capstone02.md)** | `capstone_02_review_desk.py` | **Done** |
| **4** | **[capstone04.md](capstone04.md)** | `capstone_04_research_agent.py` | **Done** |
| 5 | `capstone05.md` (later) | `capstone_05_full_stack_mini.py` | Optional |

One folder · **one guide `.md` per capstone** · Capstone 1 uses **two scripts** (ingest + chat).

---

## Before any capstone

1. Run `D:\py_venv\rag_application_builder_foundation\set_env.ps1`
2. `cd D:\Workarea\learning\playground\langchain`
3. Open the capstone’s **own** `.md` guide (e.g. [capstone01.md](capstone01.md))
4. Skim linked reference modules — then **close** them when you type

**Memory hook (every capstone):** `from watson_llm import make_watsonx_llm` — OpenAI backend (see [PROVIDER_SWAP_WATSON_TO_OPENAI.md](../PROVIDER_SWAP_WATSON_TO_OPENAI.md)).

---

## What each capstone covers (ideas)

| # | Name | Main ideas from labs |
|---|------|----------------------|
| 1 | [RAG Tutor](capstone01.md) | Load → split → embed → Chroma → QA (23–31) |
| 2 | [Review Desk](capstone02.md) | Multi-step chain + JSON (34, 11, 18) |
| 3 | [Remember-Me Chat](capstone03.md) | Chat template + memory (20, 33) |
| 4 | [Research Agent](capstone04.md) | Agent + tools + RAG tool (35 + #1) |
| 5 | Full Stack Mini | All modes in one CLI |

**Suggested order:** 1 → 3 → 2 → 4 → 5

---

## Grok rhythm

- One **bite** per message in the `.py` file  
- Reference **closed** when rebuilding from memory  
- Log traps → `courses/crs_001/.../docs/TRAINING_LOG.md`

**CRS 001 course:** complete (2026-06-19). Docs: `courses/crs_001/.../docs/CAPSTONE_CODE_GUIDE.md` · bubbles: `crs_001_capstone_flows.html`

**Optional next:** capstone 5 full-stack mini — deferred.