# Module 2 — Build Apps with RAG (Gradio)

**After M1:** You have RAG in Python. M2 puts a **web UI** on it.

## Read order (before coding)

**Full file-by-file walkthrough:** `../../source_cards/by_file/00-INDEX.md` — one card per file, every section.

| Order | File | Walkthrough |
|------:|------|-------------|
| 1 | `01.md` | `source_cards/by_file/01.md.md` |
| 2 | `02.pdf` | `source_cards/by_file/02.pdf.md` |
| 3 | `03.md` | `source_cards/by_file/03.md.md` |
| 4 | `04.pdf` | `source_cards/by_file/04.pdf.md` |
| 5 | `05.md` | `source_cards/by_file/05.md.md` |
| 6 | `06.pdf` | `source_cards/by_file/06.pdf.md` |
| 7 | `07.jpg` | `source_cards/by_file/07.jpg.md` (quiz) |
| 8 | `08.md` | `source_cards/by_file/08.md.md` |
| 9 | `09.pdf` | `source_cards/by_file/09.pdf.md` |

Coursera launchers: `03.md` (simple lab), `05.md` (QA PDF lab) — same content as 04/06 PDFs.

## M2 coding bites (local)

Run from `lab/python` after `set_env.ps1`.

| # | Script | Source | Goal |
|---|--------|--------|------|
| 1 | `09_m2_gradio_sean.py` | `01.md` | Text in → text out |
| 2 | `10_m2_gradio_file.py` | `01.md` | `gr.File` multiple upload |
| 3 | `11_m2_gradio_rag.py` | M1 + Gradio | Fixed policy doc RAG in browser |
| 4 | `12_m2_gradio_greet_slider.py` | `02.pdf` | `fn` + slider + string shortcuts |
| 4a | `12a_m2_gradio_combine_sentences.py` | `04.pdf` p.9 | Two Textbox → combine exercise |
| 5 | `13_m2_gradio_number_sum.py` | `04.pdf` | `gr.Number` sum |
| 6 | `14_m2_gradio_components.py` | `04.pdf` | **Quiz prep** — all input types |
| 7 | `15_m2_gradio_llm_chat.py` | `04.pdf` | LLM only (no retrieval) |
| 8 | `16_m2_gradio_pdf_rag.py` | `06.pdf` | Upload PDF + question |

**Study order:** `09` → `10` → `12` → `13` → `14` → *(quiz)* → `15` → `11` → `16`

## Gradio in one line

```text
Python function  +  gr.Interface(fn, inputs, outputs)  +  .launch()  =  local web page
```

CRS 001 used **Flask**; CRS 002 uses **Gradio** for ML demos — faster UI, less routing boilerplate.