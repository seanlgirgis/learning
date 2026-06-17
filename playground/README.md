# Playground

**Your space** — drills, forks, and experiments. Not part of any course curriculum.

| Layer | Path | Owner |
|-------|------|-------|
| Course labs | `courses/.../lab/python/` | Curated, quiz-aligned |
| Course experiments | `courses/.../study_pages/experiments/` | Agent teaching trials |
| **Playground** | `playground/` | **Sean** — messy is fine |

## Rules

1. Run `D:\py_venv\rag_application_builder_foundation\set_env.ps1` before Python or notebooks.
2. Never hard-code API keys — use environment variables only.
3. Copy and break things freely; nothing here is graded or canonical.
4. When an idea works, say so — we can promote it into a course `experiments/` page or lab script.

## Folders

```text
langchain/    ← prompts, LCEL, invoke drills (Course 1 now)
rag/          ← loaders, chunking, retrieval (Course 2+ soon)
notebooks/    ← your forked Coursera / personal .ipynb files
notes/        ← quick scribbles, session logs
scratch/      ← throwaway; safe to delete anytime
```

## Start here

```powershell
D:\py_venv\rag_application_builder_foundation\set_env.ps1
cd D:\Workarea\learning\playground\langchain
python .\00_env_check.py
```

Open [index.html](index.html) in a browser for links.

## Current focus

LangChain + prompt engineering (CRS 001). RAG folder is ready for when you start CRS 002.