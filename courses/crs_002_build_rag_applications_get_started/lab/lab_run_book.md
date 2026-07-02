# Lab Run Book — CRS 002

Fresh course — build evidence **module by module**. Log runs here.

## Environment

```powershell
D:\py_venv\rag_application_builder_foundation\set_env.ps1
cd D:\Workarea\learning\playground\notebooks
.\start_jupyter.ps1
```

Open: `sean_crs002_m1_rag_summarize.ipynb`

Regenerate local notebook from Coursera source:

```powershell
python D:\Workarea\learning\courses\crs_002_build_rag_applications_get_started\lab\notebooks\prepare_m1_rag_notebook.py
```

---

## Module 1 — Summarize private documents (RAG)

See `lab/python/README.md` for script map. Run from `playground/langchain`.

| Step | Script | Status |
|------|--------|--------|
| Core RAG (your build) | `02_m1_rag_sean.py` | **PASS** |
| Prompt template / don't know | `03_m1_prompt_dont_know.py` | **PASS** |
| Conversational memory + history | `04_m1_memory_chat.py` | **PASS** |
| Exercise 2 — source chunks | `05_m1_return_sources.py` | **PASS** |
| Exercise 1 — practice document | `06_m1_practice_document.py` | NOT RUN |
| REPL chat (`qa()` pattern) | `07_m1_chat_repl.py` | NOT RUN |
| Exercise 3 — model compare | `08_m1_model_compare.py` | NOT RUN |
| Reference smoke | `01_m1_rag_smoke.py` | **PASS** |

**Provider:** `watson_llm.py` (OpenAI backend) — not Skills Network / granite on IBM cloud.

**Canonical script mirror (playground):** `playground/langchain/31.rag.retrieval_qa.py` (same pattern, PDF source).

---

## Module 2 — Gradio + QA bot

Source cards: `../source_cards/` · Materials: `../source_material/module2/README.md`

Run from `lab/python` (not `playground/langchain`).

| Step | Script | Coursera source | Status |
|------|--------|-----------------|--------|
| Echo Textbox | `09_m2_gradio_sean.py` | `01.md` | |
| File upload | `10_m2_gradio_file.py` | `01.md` | |
| Greet + slider | `12_m2_gradio_greet_slider.py` | `02.pdf` | |
| Number sum | `13_m2_gradio_number_sum.py` | `04.pdf` | |
| Component zoo | `14_m2_gradio_components.py` | `04.pdf` | |
| LLM chat UI | `15_m2_gradio_llm_chat.py` | `04.pdf` | |
| Policy RAG UI | `11_m2_gradio_rag.py` | M1 + Gradio | |
| PDF upload RAG | `16_m2_gradio_pdf_rag.py` | `06.pdf` | |

**Quiz prep:** read `source_cards/03-m2-gradio-quiz.md` after script `14`.

---

## Module 3 — LlamaIndex (local track)

**Folder:** `lab/module3/` — labs `01`–`03` (see `README.md`)  
**Env:** `set_env.ps1` + OpenAI mini (Proxycurl/watsonx SN Labs workarounds in README)

| Lab | Script | Status |
|------|--------|--------|
| 01 Ingest | `module3/lab_01_ingest.py` | |
| 02 Index + query | `module3/lab_02_index_query.py` | |
| 03 Icebreaker REPL | `module3/lab_03_icebreaker.py` | |
| optional UI | `module3/lab_03_icebreaker_ui.py` | |