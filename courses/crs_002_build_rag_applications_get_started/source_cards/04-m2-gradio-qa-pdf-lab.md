# M2 — QA bot over PDF (`06.pdf`)

## Pipeline (build order in `qabot.py`)

```text
PyPDFLoader(file) → RecursiveCharacterTextSplitter → Chroma + embeddings → retriever
→ RetrievalQA(llm, retriever) → answer string → Gradio Textbox
```

| Step | Course class | Your local script |
|------|--------------|-------------------|
| Load PDF | `PyPDFLoader(file.name)` | same |
| Split | `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)` | same |
| Embed + store | `Chroma.from_documents(chunks, embedding_model)` | `make_watsonx_embeddings()` |
| Retrieve | `vectordb.as_retriever()` | same |
| Answer | `RetrievalQA.from_chain_type(..., chain_type="stuff")` | `make_llm()` |

Course rebuilds the index **on each question** inside `retriever_qa` — slow but matches the lab.

## Gradio layout (two inputs)

```python
inputs=[
    gr.File(label="Upload PDF", file_count="single", file_types=[".pdf"]),
    gr.Textbox(label="Question", lines=2),
]
outputs=gr.Textbox(label="Answer")
```

`fn(file, query)` — **two parameters** → **two input components**, same order.

## vs script `11_m2_gradio_rag.py`

| | 11 (policies) | 16 (PDF upload) |
|---|---------------|-----------------|
| Document | Fixed `.txt` at startup | User uploads PDF each session |
| Inputs | Question only | **File + Question** |
| Ingest | Once at launch | Per submit (course pattern) |

## Local script

`16_m2_gradio_pdf_rag.py` — upload a **small** PDF for best results (course warning).