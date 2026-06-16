# Source Cards (RemNote Import)

These Markdown files are **import sources for RemNote** — not primary study material. Read theory in `study_pages/` first; import cards to reinforce recall.

Format spec: `../../../planning/remnote_source_cards.md`

## Import order

| # | File | Layer | Cards |
|---|------|-------|------:|
| 1 | `01 coursera_ibm_rag_dev...undations_learning_mode.md` | Theory — generative vs discriminative, foundation models, LLMs | 15 |
| 2 | `02 coursera_ibm_rag_dev...echniques_learning_mode.md` | Theory — prompt engineering techniques | 20 |
| 3 | `03 coursera_ibm_rag_dev...ates_chat_learning_mode.md` | Theory — prompt templates and chat templates | 20 |
| 4 | `04 coursera_ibm_rag_dev...s_parsers_learning_mode.md` | Theory — LCEL, runnables, parsers | 25 |
| 5 | `05_01_prompt_and_chat_coding.md` | Code — PromptTemplate, ChatPromptTemplate | 15 |
| 6 | `05_02_few_shot_and_lcel_coding.md` | Code — few-shot, LCEL pipelines | 15 |
| 7 | `05_03_parallel_json_structured_coding.md` | Code — RunnableParallel, JSON, structured output | 16 |
| 8 | `05_04_history_and_provider_coding.md` | Code — history, provider switching | 15 |
| 9 | `05_05_selective_reinforcement.md` | Mixed — invoke rules, self-consistency, traps | 19 |
| 10 | `05_06_invoke_and_vocabulary.md` | Invoke trio, format/invoke, roles, template pair rule | 12 |

**Total: 172 cards**

## Card formats

**Multiple choice** — correct option marked with `>>A)`:

```markdown
- Question text? >>A)
    - Correct answer
    - Distractor
```

**Cloze** — answer after arrow:

```markdown
- Complete: `prompt.__________({"topic": "RAG"})`→invoke
```

## RemNote import steps

1. Open RemNote → Import (or paste into a document).
2. Import files **in table order** (01 → 05_05).
3. Place under a course document, e.g. `CRS 001 — Develop Generative AI`.
4. Review daily after reading the matching `study_pages/` chapter and running `lab/python/` examples.

Filenames `01`–`04` keep RemNote export truncation (`...`) — do not rename unless you re-export from RemNote.