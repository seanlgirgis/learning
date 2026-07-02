# Module 1 — What is RAG

**Course:** CRS 002 · IBM · Build RAG Applications: Get Started  
**Hands-on:** Notebook — *Summarize Private Documents Using RAG, LangChain, and LLMs* (~45 min)

---

## Read order (materials pass)

Do these **before** the notebook. Skim repeats from CRS 001 — focus on **where each idea sits in the RAG pipeline**.

| Order | File | What you get |
|------:|------|----------------|
| 1 | `01.v.md` | Course intro — why RAG, 3 modules, lab preview |
| 2 | `02.md` | Official outline — M1 topics + tool list (LangChain, Granite, Python) |
| 3 | `05.md` | **Why RAG** — hallucination, out-of-date answers, content store (Marina Danilevsky) |
| 4 | `06.md` | **RAG pipeline** — embed → retrieve → augment → generate; chunking; dot vs cosine |
| 5 | `11.md` | **Module summary** — recall checklist after videos |
| 6 | `08.md` | Coursera lab launcher (reference only — we run **local** copy) |

**Optional / skip for now:** `03.md` (whole cert map), `14.md` (discussion forum), PDFs/images (`04.png`, `07.pdf`, `10.assignment.jpg`, `13.pdf`).

---

## RAG pipeline (stick this)

```text
Documents → split chunks → embed → vector store (Chroma)
User question → embed → retrieve top-k chunks → augment prompt → LLM answer
```

**Two components:** Retriever + Generator.

---

## Notebook map (coding pass)

Local copy: `lab/notebooks/sean_crs002_m1_rag_summarize.ipynb`  
Playground copy: `playground/notebooks/sean_crs002_m1_rag_summarize.ipynb`

| Step | Notebook section | Concepts |
|------|------------------|----------|
| 1 | Setup | Imports, warnings |
| 2 | Preprocessing | Download `companyPolicies.txt`, preview |
| 3 | Splitting | `TextLoader` + `CharacterTextSplitter` |
| 4 | Embedding & storing | Embeddings → `Chroma.from_documents` (**Indexing**) |
| 5 | LLM | Local `make_watsonx_llm()` (OpenAI via `watson_llm` shim) |
| 6 | RetrievalQA | `qa.invoke("what is mobile policy?")` |
| 7 | Prompt template | "don't know" when answer not in doc |
| 8 | Memory | `ConversationalRetrievalChain` + `history` |
| 9 | Exercises 1–3 | Your doc · return sources · try another model |

Run book: `../../lab/lab_run_book.md`

**Script map (notebook gaps):** `../../lab/python/README.md`

| Script | Covers |
|--------|--------|
| `02_m1_rag_sean.py` | Core pipeline (yours) |
| `03_m1_prompt_dont_know.py` | PromptTemplate |
| `04_m1_memory_chat.py` | ConversationalRetrievalChain |
| `05_m1_return_sources.py` | Exercise 2 |
| `06_m1_practice_document.py` | Exercise 1 |
| `07_m1_chat_repl.py` | REPL wrapper |
| `08_m1_model_compare.py` | Exercise 3 (local OpenAI models) |

---

## After M1 (not yet)

- Coursera module quiz + graded assessment  
- RemNote deck `01` (RAG theory) + `02` (M1 lab)  
- Bubble map: RAG pipeline (optional)