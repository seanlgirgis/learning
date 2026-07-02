# Local OpenAI Icebreaker Bot Lab

A bite-by-bite learning project that mirrors the Coursera **AI Icebreaker Bot with LlamaIndex + IBM watsonx** lab. The RAG architecture is the same; this version swaps watsonx for **OpenAI**.

## Purpose

Build a small profile Q&A app that:

1. Loads LinkedIn-style profile data (mock JSON by default)
2. Splits it into searchable chunks (nodes)
3. Embeds chunks into a vector index (searchable memory)
4. Uses a query engine to retrieve relevant chunks and ask an LLM for answers

Safe sentence: **We changed the provider, not the RAG architecture.**

## Mental model

```text
extraction     → load profile data (dict)
Document       → loaded text object (profile JSON string)
node / chunk   → smaller searchable piece
embedding      → semantic fingerprint (vector)
index          → searchable memory (VectorStoreIndex)
query engine   → finds relevant chunks + builds prompt
LLM            → writes the final answer
```

## Project map

```text
openai_icebreaker_local_lab/
├── README.md                 ← start here
├── bootstrap.py              ← import path helper (used by main/app/modules)
├── config.py                 ← prompts, chunk size, model names (no API calls)
├── main.py                   ← CLI: full pipeline + terminal chat
├── app.py                    ← Gradio web UI
├── data/
│   └── mock_linkedin_profile.json   ← used when mock=True
├── modules/
│   ├── data_extraction.py    ← extraction (mock or Proxycurl)
│   ├── data_processing.py    ← Document → chunks → embeddings → index
│   ├── llm_interface.py      ← OpenAI clients (replaces watsonx)
│   └── query_engine.py       ← retriever + prompt + LLM
├── tests/                    ← run in order (see below)
└── docs/
    ├── PROJECT_MAP.md
    ├── OPENAI_VS_WATSONX_MAPPING.md
    ├── PLAY_BY_PLAY_INDEX.md
    └── play_by_play/         ← step-by-step study guides
```

See also: [docs/PROJECT_MAP.md](docs/PROJECT_MAP.md) and [docs/play_by_play/00_big_picture.md](docs/play_by_play/00_big_picture.md).

## What changed from Coursera?

| Coursera lab | Local version |
|---|---|
| IBM watsonx LLM | OpenAI LLM |
| IBM watsonx embeddings | OpenAI embeddings |
| Cloud IDE `/home/project/icebreaker` | This folder on your machine |
| watsonx project ID + URL | `OPENAI_API_KEY` |
| Mock LinkedIn profile | `data/mock_linkedin_profile.json` |

Details: [docs/OPENAI_VS_WATSONX_MAPPING.md](docs/OPENAI_VS_WATSONX_MAPPING.md)

## Setup

### Option A — shared learning venv (recommended)

```powershell
. D:\py_venv\rag_application_builder_foundation\set_env.ps1
cd D:\Workarea\learning\courses\crs_002_build_rag_applications_get_started\lab\openai_icebreaker_local_lab
pip install -r requirements.txt
```

`set_env.ps1` sets `OPENAI_API_KEY`, `OPENAI_MODEL`, and embedding model names.

### Option B — project `.env`

```bash
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add your OpenAI API key. Never commit real keys.

## Test order (and token caution)

Run from the project folder. **Start with free tests** (no OpenAI calls):

| Order | Command | OpenAI cost |
|---|---|---|
| 1 | `python tests/test_environment.py` | None |
| 2 | `python tests/test_config.py` | None |
| 3 | `python tests/test_data_extraction.py` | None (mock JSON only) |
| 4 | `python tests/test_llm_interface_imports.py` | None (imports only) |
| 5 | `python tests/test_data_processing.py` | **Embeddings** |
| 6 | `python tests/test_query_engine.py` | **Embeddings + LLM** |

Mock mode (`mock=True` in tests) means:

- Reads `data/mock_linkedin_profile.json`
- Does **not** call LinkedIn
- Does **not** call Proxycurl

OpenAI may still be called in tests 5 and 6 for embeddings and answers.

## Run the CLI

```bash
python main.py --mock
```

Pipeline: extraction → chunks → index → icebreaker facts → terminal chat.

Try asking: `What is this person known for?`  
Exit with: `exit`, `quit`, or `bye`.

## Run the Gradio app

```bash
python app.py
```

Open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

1. Keep **Use Mock Data** checked
2. Click **Process Profile**
3. Switch to **Chat** and ask a question

## Study path

Work through [docs/PLAY_BY_PLAY_INDEX.md](docs/PLAY_BY_PLAY_INDEX.md) in order while running the matching tests and reading each module.

## Safety rules

- Never put API keys in source code
- Use mock mode while learning extraction and imports
- Run embedding/LLM tests only when you accept token cost
- This beginner version rebuilds the index each run (simple, not production-efficient)