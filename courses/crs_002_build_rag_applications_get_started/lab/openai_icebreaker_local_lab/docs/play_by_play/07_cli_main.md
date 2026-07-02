# 07 — CLI Main App

**File:** `main.py`

## Goal

Run the full pipeline in the terminal with mock data.

## Command

```bash
python main.py --mock
```

## What happens

1. **Extraction** — mock JSON (no OpenAI)
2. **Split** — nodes/chunks (no OpenAI)
3. **Index** — OpenAI embeddings
4. **Facts** — query engine + OpenAI LLM
5. **REPL** — each question uses RAG + LLM

## Try asking

```text
What is this person known for?
Where did they study?
```

Exit: `exit`, `quit`, or `bye`

## Flags

| Flag | Meaning |
|---|---|
| `--mock` | Use local JSON |
| `--url` | LinkedIn URL (live mode) |
| `--api-key` | Proxycurl key (live mode) |
| `--model` | Override OpenAI LLM name |

## Cost note

Every full run rebuilds the index and calls OpenAI. Fine for learning; production would persist the index.

## Next step

[08_gradio_app.md](08_gradio_app.md)