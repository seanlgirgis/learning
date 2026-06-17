# LangChain playground

Drills for CRS 001 — prompt templates, chat roles, LCEL, providers.

**LangChain reference:** [../../reference/langchain/index.html](../../reference/langchain/index.html) — 11 modules, 14 recipes; scripts stay here.

## Lab track (Coursera notebook → local)

| Lab | Script | Reference |
|-----|--------|-----------|
| 15 | `15.watson_helper.generate_test.py` | [IBM generate](../../reference/langchain/recipes/ibm-model-generate.html) |
| 16 | `16.langchain_helper.invoke_test.py` | [LLM plug-in](../../reference/langchain/recipes/langchain-llm-plug.html) |
| 17 | `17.chat_messages.invoke_test.py` | [Chat messages](../../reference/langchain/recipes/chat-messages.html) |
| 18 | `18.temperature.compare.py` | [Temperature](../../reference/langchain/recipes/temperature-compare.html) |
| 19 | `19.params.py` | [String template](../../reference/langchain/recipes/string-template-demo.html) |
| 20 | `20.chat_prompt_templates.py` | [Chat template](../../reference/langchain/recipes/chat-prompt-template.html) |
| 21 | `21.output_parsers.py` | [JSON Joke](../../reference/langchain/recipes/json-joke-parser.html) · [Comma list](../../reference/langchain/recipes/comma-list-parser.html) |
| 22 | `22.exercise2.movie_json.py` | [Movie JSON](../../reference/langchain/recipes/movie-json.html) |
| 28–31 | embeddings → Chroma → retriever → RetrievalQA | Labs 28–31 in `playground/langchain/` |
| 32 | `32.parent_document_retriever.py` | Parent doc retriever (notebook section) |

Earlier LCEL drills: `08.lcel.1.py` … `14.lcel.chain.custom_formatting.py` — see [recipes index](../../reference/langchain/recipes/index.html).

## Suggested drills (add your own files)

| Idea | Try |
|------|-----|
| `format` vs `invoke` | Copy a line from `courses/.../lab/python/01_*.py` and call both |
| `human` vs `user` | Same prompt, two `ChatPromptTemplate` variants |
| Pipe shape | `prompt \| model \| parser` without caring about output quality |
| Provider swap | Same chain, swap OpenAI / Watsonx model object only |

## Canonical reference (read-only)

- `courses/crs_001_develop_generative_ai_applications_get_started/lab/python/`
- `courses/crs_001_develop_generative_ai_applications_get_started/source_cards/05_06_invoke_and_vocabulary.md`

## Shared watsonx helper

Import `llm_model` from **`watson_llm.py`** in any script in this folder:

```python
from watson_llm import GenParams, llm_model

response = llm_model("What is RAG?")
response = llm_model("Be creative.", params={"temperature": 0.9})
```

Examples: `02_watson_llm.py`, `try_import_watson_llm.py`, `drill_llm_model_local.py`.

## LCEL pipe (plug in objects)

```python
from langchain_core.prompts import PromptTemplate
from lcel_pipe import str_chain
from watson_llm import make_watsonx_chat

prompt = PromptTemplate.from_template("Topic: {topic}\nExplain briefly.")
model = make_watsonx_chat()          # build once
chain = str_chain(prompt, model)     # prompt | model | StrOutputParser
chain.invoke({"topic": "LCEL"})
```

See `lcel_pipe.py` (reusable) and `try_lcel_pipe.py` (examples).

## Run

```powershell
D:\py_venv\rag_application_builder_foundation\set_env.ps1
cd D:\Workarea\learning\playground\langchain
python .\00_env_check.py
python .\01_import_probe.py
python .\try_import_watson_llm.py
```

## Coursera notebook vs this venv

Coursera pins **langchain 0.2.x**; foundation venv uses **1.x**. Do not paste the notebook import block into `00_env_check.py` — that file only checks env vars.

If a cell says `from langchain.chains import LLMChain`, use **`langchain_classic`** instead. Full table: [coursera_import_map.md](coursera_import_map.md).

Name new scripts `drill_*.py` or `try_*.py` so they are easy to spot as yours.