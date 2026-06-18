# Capstones — index

**What this folder is:** Your **practice apps** — not copy-paste labs. One `.py` per project. You type each bite; Grok coaches.

**Where:** `playground/langchain/capstone/`  
**Full plan:** [planning/langchain_capstone_projects.md](../../../planning/langchain_capstone_projects.md)

---

## Start here

| # | Guide | Script | Status |
|---|--------|--------|--------|
| **1** | **[capstone01.md](capstone01.md)** | `capstone_01_ingest.py` (you type) + notebook | Ready — **start here** |
| 2 | `capstone02.md` (later) | `capstone_02_review_desk.py` | Not yet |
| 3 | `capstone03.md` (later) | `capstone_03_remember_me_chat.py` | Not yet |
| 4 | `capstone04.md` (later) | `capstone_04_research_agent.py` | Not yet |
| 5 | `capstone05.md` (later) | `capstone_05_full_stack_mini.py` | Optional |

One folder · **one guide `.md` per capstone** · Capstone 1 uses **two scripts** (ingest + chat).

---

## Before any capstone

1. Run `D:\py_venv\rag_application_builder_foundation\set_env.ps1`
2. `cd D:\Workarea\learning\playground\langchain`
3. Open the capstone’s **own** `.md` guide (e.g. [capstone01.md](capstone01.md))
4. Skim linked reference modules — then **close** them when you type

**Memory hook (every capstone):** Route B — `from watson_llm import make_watsonx_llm` for pipes and RAG.

---

## What each capstone covers (ideas)

| # | Name | Main ideas from labs |
|---|------|----------------------|
| 1 | [RAG Tutor](capstone01.md) | Load → split → embed → Chroma → QA (23–31) |
| 2 | Review Desk | Multi-step chain + JSON (34, 11, 18) |
| 3 | Remember-Me Chat | Chat template + memory (20, 33) |
| 4 | Research Agent | Agent + tools + RAG tool (35 + #1) |
| 5 | Full Stack Mini | All modes in one CLI |

**Suggested order:** 1 → 3 → 2 → 4 → 5

---

## Grok rhythm

- One **bite** per message in the `.py` file  
- Reference **closed** when rebuilding from memory  
- Log traps → `courses/crs_001/.../docs/TRAINING_LOG.md`

**Next:** open [capstone01.md](capstone01.md) → say **bite 1** in chat.