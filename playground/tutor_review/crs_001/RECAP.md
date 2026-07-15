# CRS 001 tutor recap (Module 1 core)

Memorize these five blocks. Then Module 2 (LCEL deeper) is easier.

## 1. Two kinds of AI

```text
discriminative → decide / label / score
generative     → write / draft / invent
```

## 2. Foundation model vs LLM

```text
LLM ⊂ foundation models
Language job → say LLM
Vs narrow single-task model → say foundation model
```

## 3. Prompt engineering

```text
Runtime control of a fixed model (not retraining)
Pieces: instructions · context · examples · constraints · output shape
shots: 0 = zero · 1 = one · 2+ = few
self-consistency = several samples + agree
```

## 4. Templates

```text
from_template  → blanks in ONE string (no turns)
from_messages  → blanks + turns (system / human / ai)
blanks live in content (any role OK)
invoke({dict}) → FILL blanks (both)
```

## 5. Invoke trio + billing

```text
prompt.invoke  → prepare (no model charge)
model.invoke   → call LLM once (charges)
chain.invoke   → prompt | model | parser (charges)

ChatOpenAI(...) only builds the client — free until invoke
```

## 6. LCEL (Module 2 start)

```text
LCEL = LangChain Expression Language
|    = connect runnables left → right
chain = an LCEL program (itself a runnable)
prompt | model | StrOutputParser()  → prepare → generate → plain string
dependent steps → sequence (|)
independent steps → parallel (RunnableParallel)
StrOutputParser → plain string
Json / structured → fields for code (Flask, APIs)
MessagesPlaceholder → slot for a list of turns (not storage)
History grow/trim / N+vector M → your app (or memory layer)

chain   = fixed pipe (A→B→C)
memory  = conversation notebook
agent   = LLM picks tools/actions
one ask → append HumanMessage + AIMessage (+2)

Module 3: model.py = brain · app = HTTP door · JSON fields for APIs

RAG: retrieve → augment prompt → generate
Build: Source→…→Index · Query: Retrieve→LLM→Answer
Chunk = piece · Embedding = meaning vector · Retrieve = nearest chunks

## 7. CRS 003 Module 1 (started)

```text
embedding = numeric meaning vector
next: vector DB vs SQL · metrics · Chroma
field guide: courses/crs_003_.../study_pages/module1_field_guide.html
```


## Tutor files (run order)

| # | File | LLM? |
|---|------|------|
| 01 | `01_prompt_template_fill.py` | no |
| 02 | `02_chat_prompt_template_fill.py` | no |
| 1b | `01b_prompt_template_with_llm.py` | yes |
| 2b | `02b_chat_prompt_with_llm.py` | yes |
| 03 | `03_few_shot_prompt.py` | fill + yes |

Folder: `playground/tutor_review/crs_001/`
