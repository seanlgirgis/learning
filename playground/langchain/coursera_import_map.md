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
- Exercises 3–4, 7: may need `langchain-community` (document loaders, Chroma) — install when you reach those

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