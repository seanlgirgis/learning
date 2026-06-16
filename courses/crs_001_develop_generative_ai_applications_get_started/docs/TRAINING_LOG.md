# Training Log — CRS 001

Sean study questions and recall tracking. Agent appends rows during training sessions.

**Tally and backlog:** `COURSE_OPERATIONS.md` (same folder)

| Date | Topic | Question / source | Sean's answer | Correct | Confusion pattern | Status |
|------|-------|-------------------|---------------|---------|-------------------|--------|
| 2026-06-15 | LangChain · ChatPromptTemplate | RemNote `05_01` — which property holds the generated message list after `invoke`? | Leaning `messages.output` (screenshot) | `messages.messages` | Mixing invoke return shape with chain/parser `.output` | needs_repetition |
| 2026-06-15 | LangChain · ChatPromptTemplate | RemNote `05_01` cloze — `ChatPromptTemplate.__________((...))` | (asked via image) | `from_messages` | — | new |
| 2026-06-15 | LangChain · ChatPromptTemplate | RemNote `05_01` — which tuple is the current user request? | (asked via image) | `("human", "{question}")` | — | new |
| 2026-06-15 | LangChain · roles | Sean: trained on system/user/assistant; first time seeing `human` | Prior mental model = user | LangChain says `human` | API vs template vocabulary | needs_repetition |
| 2026-06-15 | LangChain · PromptTemplate | RemNote `05_01` cloze — `PromptTemplate.__________("Explain {topic}.")` | drill: `FromTemplate` → concept OK | `from_template` | Spelling: snake_case | improving |
| 2026-06-15 | LangChain · ChatPromptTemplate | drill — `ChatPromptTemplate.__________([("human", "{q}")])` | `from_template` then **`from_messages`** ✓ | `from_messages` | Brackets = list = from_messages | solid |
| 2026-06-15 | Coursera crs_001 quiz | Module quiz (5 Q) — in-context learning, zero-shot, LCEL pipe, PromptTemplate | **100%** (screenshot) | all correct | RemNote drills translating to platform | solid |
| 2026-06-15 | Coursera crs_001 quiz | Module quiz (7 Q) — prompt elements, format(), LCEL coercion, in-context, pipe | **100%** (screenshot) | all correct | Platform uses `format()` vocabulary; labs use `invoke()` | solid |

## Concepts to revisit

- **`chat_prompt.invoke()` return** → use `.messages` for the message list (lab `03_chat_prompt_template.py`)
- **Invoke trio** — `prompt.invoke` = prepare · `model.invoke` = generate · `chain.invoke` = run all (RemNote `05_05`)
- **Role naming** — Sean trained on `system / user / assistant`; LangChain templates use `system / human / ai` (same idea, different words)

## Next micro-drill (when ready)

1. **String template:** `PromptTemplate.__________("Explain {topic}.")` → ?
2. **Chat template:** `ChatPromptTemplate.__________([("human", "{q}")])` → ?
3. After `formatted = prompt.invoke({"topic": "RAG"})`, print text with `formatted.__________()` → ?