# Module 3 — LlamaIndex (local)

Three labs. Read the study card, run the script, read the code top to bottom.

**Env (PowerShell):**

```powershell
. D:\py_venv\rag_application_builder_foundation\set_env.ps1
cd D:\Workarea\learning\courses\crs_002_build_rag_applications_get_started\lab\module3
```

## Run order

| Lab | Script | Study material | What you learn |
|-----|--------|----------------|----------------|
| 1 | `lab_01_ingest.py` | `01.md` card | Document, folder reader, splitter → nodes |
| 2 | `lab_02_index_query.py` | `02.md` card | embed + index, retriever, query engine |
| 3 | `lab_03_icebreaker.py` | `05.pdf` card | mock profile RAG + terminal chat |
| optional | `lab_03_icebreaker_ui.py` | `05.pdf` UI section | Gradio instead of SN Labs port 5000 |

**Quiz:** `source_cards/by_file/module3/06.jpg.md` after lab 2.

## Only one shared file

`config.py` — prompt templates and `CHUNK_SIZE` / `SIMILARITY_TOP_K` (same role as course `config.py`).

Everything else is **in the lab file** so you see the real LlamaIndex calls.

## Workarounds

| Course | Local |
|--------|-------|
| Proxycurl LinkedIn API | `data/mock_linkedin_profile.json` |
| watsonx on SN Labs | `OPENAI_API_KEY` + `llama-index-*-openai` |
| SN Labs `app.py` :5000 | `lab_03_icebreaker_ui.py` :7860 |

Old step-by-step scripts are in `archive/steps/` if you need them.