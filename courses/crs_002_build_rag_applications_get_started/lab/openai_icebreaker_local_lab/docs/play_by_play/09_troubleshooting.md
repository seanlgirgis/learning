# 09 — Troubleshooting

## Missing OpenAI key

**Symptom:** `OPENAI_API_KEY is missing`

**Fix:**

- Dot-source `set_env.ps1`, or
- Copy `.env.example` to `.env` and set `OPENAI_API_KEY`

Never put keys in Python source files.

## ModuleNotFoundError: No module named 'modules'

**Symptom:** Running a test fails on `from modules...`

**Fix:** Run from the project folder:

```bash
cd openai_icebreaker_local_lab
python tests/test_data_extraction.py
```

Tests use `tests/setup_imports.py` to add the project root to `sys.path`. `main.py` and `app.py` use `bootstrap.py`.

## Package import errors

```bash
pip install -r requirements.txt
```

Then rerun `python tests/test_environment.py`.

## App port already in use

Change `server_port=5000` in `app.py` if another app owns port 5000.

## Unexpected OpenAI charges

| Script | Cost |
|---|---|
| `test_environment.py` | None |
| `test_config.py` | None |
| `test_data_extraction.py` | None |
| `test_llm_interface_imports.py` | None |
| `test_data_processing.py` | Embeddings |
| `test_query_engine.py` | Embeddings + LLM |
| `main.py --mock` | Full pipeline |
| `app.py` | Full pipeline per process + per chat message |

Stick to mock mode and the first four tests while learning extraction and config.

## Index rebuilt every run

This beginner lab rebuilds the vector index each time. A production app would save the index to disk and reload it.

## Provider confusion

Coursera = watsonx. This lab = OpenAI. Same LlamaIndex RAG steps; different provider in `llm_interface.py`.