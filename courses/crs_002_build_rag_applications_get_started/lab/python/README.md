# CRS 002 — Python scripts

```powershell
. D:\py_venv\rag_application_builder_foundation\set_env.ps1
cd D:\Workarea\learning\courses\crs_002_build_rag_applications_get_started\lab\python
```

## Module 1 — RAG

| Script | Topic |
|--------|--------|
| `02_m1_rag_sean.py` | Core RAG (download → Chroma → QA) |
| `m1_rag_shared.py` | Shared ingest + `make_llm()` |
| `03_m1_prompt_dont_know.py` | PromptTemplate — don't know |
| `04_m1_memory_chat.py` | ConversationalRetrievalChain + history |
| `05_m1_return_sources.py` | `return_source_documents=True` |
| `06_m1_practice_document.py` | Alternate practice `.txt` |
| `07_m1_chat_repl.py` | Interactive REPL |
| `08_m1_model_compare.py` | Compare models |
| `01_m1_rag_smoke.py` | Smoke test |

**M1 order:** `02` → `03` → `04` → `05` → `06` → `07` → `08`

## Module 2 — Gradio

Read `../../source_cards/` first — especially before the Coursera quiz.

| Script | Topic |
|--------|--------|
| `09_m2_gradio_sean.py` | Echo — `gr.Textbox` |
| `10_m2_gradio_file.py` | `gr.File` upload |
| `12_m2_gradio_greet_slider.py` | Greet + slider (`02.pdf`) |
| `13_m2_gradio_number_sum.py` | `gr.Number` sum (`04.pdf`) |
| `14_m2_gradio_components.py` | Component zoo — **quiz prep** |
| `15_m2_gradio_llm_chat.py` | LLM chat, no RAG |
| `11_m2_gradio_rag.py` | Policy RAG in browser |
| `16_m2_gradio_pdf_rag.py` | PDF upload + RAG (`06.pdf`) |

**M2 order:** `09` → `10` → `12` → `13` → `14` → quiz → `15` → `11` → `16`

Stop each server with **Ctrl+C** before starting the next script (port 7860).