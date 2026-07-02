# Code Catalog — CRS 001 (36 exercises + 4 capstones)

**Run env (local labs):** `D:\py_venv\rag_application_builder_foundation\set_env.ps1` then `cd lab/python`  
**Module 3:** Skills Network Cloud IDE — mirror in `lab/python/module3/`  
**Capstones:** `playground/langchain/capstone/` — see [CAPSTONE_CODE_GUIDE.md](../docs/CAPSTONE_CODE_GUIDE.md)

---

## Summary

| Bucket | Count | Path |
|--------|------:|------|
| Course labs M1–M2 | 17 | `lab/python/01`–`13`, `05b`/`05c`/`05d`/`05f` |
| Module 3 + Flask prep | 16 | `lab/python/module3/`, `flask_tutorial/` |
| Capstones | 4 projects | `playground/langchain/capstone/` |
| **Runnable scripts** | **36** | (capstones add ingest/chat variants) |

---

## Module 1 — Templates (4)

| # | File | Teaches | Output |
|---|------|---------|--------|
| 01 | `01_prompt_template_one_variable.py` | `PromptTemplate.from_template`, `invoke` | Formatted string |
| 02 | `02_prompt_template_multiple_variables.py` | Multiple `{vars}` | Formatted string |
| 03 | `03_chat_prompt_template.py` | `ChatPromptTemplate.from_messages` | `.messages` list |
| 04 | `04_few_shot_prompt_template.py` | Examples in prompt | Steered format |

---

## Module 2 — LCEL & providers (13)

| # | File | Teaches |
|---|------|---------|
| 05 | `05_lcel_local_pipeline.py` | `prompt \| model \| parser` (local stand-in) |
| 05b | `05b_lcel_openai_pipeline.py` | OpenAI adapter |
| 05c | `05c_lcel_watsonx_pipeline.py` | `ChatWatsonx` pipe |
| 05d | `05d_watsonx_smallest_test.py` | Minimal watsonx invoke |
| 05f | `05f_provider_switching_lcel_pipeline.py` | Same chain, swap provider |
| 06 | `06_runnable_parallel.py` | `RunnableParallel` |
| 07 | `07_messages_placeholder.py` | `MessagesPlaceholder` |
| 08 | `08_json_parser_shape.py` | `JsonOutputParser` → dict |
| 09 | `09_provider_native_structured_output.py` | `with_structured_output` |
| 10 | `10_conversation_history_with_messages_placeholder.py` | History in template |
| 11 | `11_update_conversation_history.py` | Append turns |
| 12 | `12_reusable_chat_function_with_history.py` | Function wrapper |
| 13 | `13_runnable_with_message_history.py` | `RunnableWithMessageHistory` |

**Memory rule:** `05` before `05b`/`05c`; parsers `08` before `09`; history `10`→`13` in order.

---

## Module 3 — Watsonx + Flask (13 scripts + app bundle)

### Bite path (`module3/`)

| Bite | File | Proves |
|------|------|--------|
| 0 | `00_env_probe.py`, `01_import_smoke.py` | Env + imports |
| 1 | `02d_capital_granite_tokens.py` | PDF auth + Granite tokens |
| 2a/2b | `03_capital_llama_plain.py`, `03_capital_llama_tokens.py` | Llama dialect |
| 3 | `04_langchain_one_model.py` | `ChatWatsonx` pipe |
| 4 | `05_json_capital_parser.py` | `JsonOutputParser` |
| 5 | `genai_flask_app/config.py`, `model.py`, `llm_test.py` | 3 models + `AIResponse` |
| 6 | `genai_flask_app/app2.py` | `POST /generate` |

### Flask tutorial (local, 3)

| File | Teaches |
|------|---------|
| `flask_tutorial/01_hello.py` | `Flask`, `@app.route` |
| `flask_tutorial/02_json_route.py` | `jsonify`, query params |
| `flask_tutorial/03_post_echo.py` | `POST /generate` shape (stub) |

### Module 3 traps (documented)

- SN auth: no `api_key` in `Credentials`
- Llama ID: use Maverick on SN, not PDF `llama-3-2-11b`
- `model.py` imports `config`; `llm_test` imports `model` only
- Browser preview optional; `curl` proves stack

---

## Capstones (4) — `playground/langchain/capstone/`

| # | Scripts | Guide | Use case |
|---|---------|-------|----------|
| 1 | `capstone_01_ingest.py`, `capstone_01_chat.py` | `capstone01.md` | RAG Q&A over course PDFs |
| 2 | `capstone_02_review_desk.py` | `capstone02.md` | Multi-step review → JSON |
| 3 | `capstone_03_remember_me_chat.py` | `capstone03.md` | Session history |
| 4 | `capstone_04_research_agent.py` | `capstone04.md` | ReAct + tools |

**Provider:** `watson_llm.make_watsonx_llm()` / `make_watsonx_agent_llm()` (OpenAI shim locally).

---

## Suggested run order (first pass)

```text
01 → 04 → 05 → 05b → 08 → 10 → 13
module3 bites 1 → 6
capstones 1 → 3 → 2 → 4
```

---

## Cross-links

- Flow charts: [exercise_and_capstone_flows.md](../study_pages/exercise_and_capstone_flows.md)
- Run book: [lab_run_book.md](lab_run_book.md)
- Bubbles: [crs_001_lcel_workflow](../bubbles/outputs/crs_001_lcel_workflow.html), [crs_001_module3_flask_app](../bubbles/outputs/crs_001_module3_flask_app.html), [crs_001_capstone_flows](../bubbles/outputs/crs_001_capstone_flows.html)