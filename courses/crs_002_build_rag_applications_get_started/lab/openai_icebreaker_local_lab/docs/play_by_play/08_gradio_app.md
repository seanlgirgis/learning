# 08 — Gradio Web App

**File:** `app.py`

## Goal

Same RAG pipeline as `main.py`, in a browser UI.

## Run

```bash
python app.py
```

Open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Tabs

### Process Profile

1. Keep **Use Mock Data** checked (reads local JSON — no LinkedIn/Proxycurl)
2. Click **Process Profile**
3. Wait for three icebreaker facts (uses OpenAI embeddings + LLM)

### Chat

Ask follow-up questions. Each message runs the query engine (OpenAI cost).

## Session storage

The app stores each built index in `active_indices` keyed by a hidden session id. If you restart the server, process the profile again.

## Next step

[09_troubleshooting.md](09_troubleshooting.md)