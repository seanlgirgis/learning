# LlamaIndex Module 3 Runbook

## Mental model

Build time:

Source files → Loader → Documents → Chunks/Nodes → Embeddings → Index / Vector Store

Ask time:

Question → Retriever → Relevant chunks → GenAI Model / LLM → Answer

## Exercise 1 — Loader

Goal: prove that files become `Document` objects.

Run:

```bash
python starter_code/01_load_documents.py
```

Look for:
- How many documents loaded
- Which file each document came from
- Small preview of each document

## Exercise 2 — Index and query engine

Goal: prove that documents become a searchable RAG index.

Run:

```bash
python starter_code/02_build_index_query.py
```

Try these questions:

```text
What is the support escalation rule for Sev-1 incidents?
What should an employee do before uploading a confidential document?
Which product is better for dashboard-style reports?
What changed after the May 2026 analytics outage?
```

## Exercise 3 — Retrieval thinking

Ask a question and then ask yourself:

1. Which source document probably answered this?
2. Which chunk probably matched?
3. Did the answer come from the document or from model guessing?

## Exercise 4 — Add your own document

Create a new `.md` file under:

```text
data/company_knowledge/
```

Then rerun the script.

Question:
Did your new file become part of the searchable knowledge base?
