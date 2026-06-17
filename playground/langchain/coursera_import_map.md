# Coursera notebook imports → foundation venv

Coursera labs pin **langchain 0.2.11**. Your foundation venv uses **langchain 1.x** (newer, better for local CRS 001 labs).

Most notebook cells work unchanged. **Legacy chains** need a different import path.

## Translation table

| Coursera notebook writes | Use in foundation venv |
|--------------------------|------------------------|
| `from langchain.chains import LLMChain` | `from langchain_classic.chains import LLMChain` |
| `from langchain.chains import SequentialChain` | `from langchain_classic.chains import SequentialChain` |
| `from langchain.chains import LLMChain, SequentialChain` | `from langchain_classic.chains import LLMChain, SequentialChain` |
| `from langchain.memory import ConversationBufferMemory` | `from langchain_classic.memory import ConversationBufferMemory` |
| `from langchain_core.prompts import ...` | **Same** |
| `from langchain_ibm import WatsonxLLM` | **Same** |
| `from langchain.text_splitter import CharacterTextSplitter` | `from langchain_text_splitters import CharacterTextSplitter` |
| `from langchain.text_splitter import RecursiveCharacterTextSplitter` | `from langchain_text_splitters import RecursiveCharacterTextSplitter` |
| `from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter` | `from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter` |
| `from langchain.vectorstores import Chroma` | `from langchain_community.vectorstores import Chroma` |
| `from langchain.output_parsers import CommaSeparatedListOutputParser` | `from langchain_classic.output_parsers import CommaSeparatedListOutputParser` |
| `from langchain_core.pydantic_v1 import BaseModel, Field` | `from pydantic import BaseModel, Field` |
| `retriever.get_relevant_documents(query)` | `retriever.invoke(query)` |
| `from langchain.chains import RetrievalQA` | `from langchain_classic.chains import RetrievalQA` |
| `qa.run(query)` | `qa.invoke(query)` |

## What does not need changing

- `PromptTemplate`, `ChatPromptTemplate`, `StrOutputParser`
- `RunnablePassthrough`, `RunnableLambda`, pipe `|` chains (LCEL)
- `HumanMessage`, `SystemMessage`
- `WatsonxLLM`, `GenTextParamsMetaNames`

## Context notebook (Module 1)

Exercise 5 uses LCEL only — **no LLMChain**. You can run it locally after swapping Watson credentials for your `WATSONX_*` env vars.

## LangChain notebook (Module 2)

- Exercises 1–2: mostly `langchain_core` — works as-is
- Exercise 6: `LLMChain` / `SequentialChain` — use `langchain_classic` imports above
- Exercise 5: `ConversationBufferMemory` — use `langchain_classic`
- Documents / splitters / Chroma: use table above (`langchain_text_splitters`, `langchain_community`)
- Exercise 3 retriever: `invoke` not `get_relevant_documents`
- Exercises 3–4, 7: `langchain-community` + `chromadb` (already in foundation venv)

## One-time package for classic chains

```powershell
pip install langchain-classic
```

Then run:

```powershell
python .\01_import_probe.py
```

## Or run unchanged in Coursera

Skills Network has 0.2.11 pre-pinned — `from langchain.chains import LLMChain` works there with no edits.