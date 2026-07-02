# Project Map

Where each file fits in the RAG pipeline.

## Folder layout

```text
openai_icebreaker_local_lab/
├── README.md
├── bootstrap.py              # sys.path setup for imports
├── requirements.txt
├── .env.example
├── config.py                 # settings + prompt templates
├── main.py                   # CLI entry point
├── app.py                    # Gradio entry point
├── data/
│   └── mock_linkedin_profile.json
├── modules/
│   ├── __init__.py
│   ├── data_extraction.py    # extraction
│   ├── data_processing.py    # chunks + embeddings + index
│   ├── llm_interface.py      # OpenAI clients
│   └── query_engine.py       # RAG answers
├── tests/
│   ├── setup_imports.py
│   └── test_*.py
└── docs/
```

## Pipeline map

| Step | Mental model | File | OpenAI? |
|---|---|---|---|
| 1 | extraction | `modules/data_extraction.py` | No |
| 2 | Document → nodes/chunks | `modules/data_processing.py` (`split_profile_data`) | No |
| 3 | embeddings → index | `modules/data_processing.py` (`create_vector_database`) | Yes (embeddings) |
| 4 | LLM + embedding clients | `modules/llm_interface.py` | When called |
| 5 | query engine → answer | `modules/query_engine.py` | Yes (embed + LLM) |
| 6 | CLI | `main.py` | Yes (full run) |
| 7 | Web UI | `app.py` | Yes (full run) |

## Settings

`config.py` holds chunk size, top-k, model names, mock path, and prompt templates. It does not call APIs.

## Mock data

`mock=True` always reads `data/mock_linkedin_profile.json`. No LinkedIn. No Proxycurl.

## Provider note

Coursera used IBM watsonx. This lab uses OpenAI via `llm_interface.py`. LlamaIndex classes (`Document`, `VectorStoreIndex`, `as_query_engine`) stay the same.