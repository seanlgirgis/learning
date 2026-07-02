# Exercise & Capstone Flow Charts — CRS 001

Mermaid diagrams for **use-case flow**. Pair with [CODE_CATALOG.md](../lab/CODE_CATALOG.md) for file names.

---

## Module 1 — Prompt layer

```mermaid
flowchart TD
  A[User question with variables] --> B[PromptTemplate.from_template]
  B --> C[prompt.invoke dict]
  C --> D[Formatted string]
  D --> E[model.invoke or chain]

  F[Chat roles needed] --> G[ChatPromptTemplate.from_messages]
  G --> H[prompt.invoke → .messages]

  I[Need examples in prompt] --> J[FewShotPromptTemplate / lab 04]
```

**Labs:** `01` → `02` → `03` → `04`

---

## Module 2 — LCEL pipeline

```mermaid
flowchart LR
  subgraph build [Build order]
    T[Define template with vars] --> PT[PromptTemplate]
    PT --> P[prompt]
    P --> M[model adapter]
    M --> PAR[StrOutputParser or JsonOutputParser]
    PAR --> CH[chain = p | m | par]
  end
  CH --> INV[chain.invoke input dict]
  INV --> OUT[text or dict]
```

**Provider branch:**

```mermaid
flowchart TD
  CHAIN[Same chain shape] --> O[05b OpenAI]
  CHAIN --> W[05c 05d 05f watsonx]
  CHAIN --> L[05 local stand-in]
```

**Labs:** `05` → `05b`/`05c`/`05d`/`05f` → `06` parallel → `07`–`09` parsers → `10`–`13` history

---

## Module 3 — Cloud IDE → Flask app

```mermaid
flowchart TD
  subgraph phase0 [Phase 0 probe]
    P0[venv + ibm-watsonx-ai]
    P1[02d granite tokens]
    P2[03 llama plain vs tokens]
  end
  subgraph phase1 [Phase 1 LangChain]
    P3[04 pipe StrOutputParser]
    P4[05 JsonOutputParser dict]
  end
  subgraph phase2 [Phase 2 app]
    C[config.py]
    M[model.py 3 models]
    T[llm_test.py]
    A[app2.py Flask]
  end
  phase0 --> phase1 --> phase2
  C --> M
  M --> T
  M --> A
```

**Auth trap:** `Credentials(url only)` + `project_id=skills-network` — no `api_key` in code on SN.

---

## Capstone 01 — RAG Tutor

```mermaid
flowchart LR
  subgraph ingest [capstone_01_ingest.py]
    PDF[PDFs / corpus] --> LOAD[load split]
    LOAD --> EMB[embed]
    EMB --> CHROMA[(Chroma)]
  end
  subgraph chat [capstone_01_chat.py]
    Q[User question] --> RET[retrieve top-k]
    RET --> CTX[stuff context]
    CTX --> QA[prompt | llm]
    QA --> A[Answer]
  end
  CHROMA --> RET
```

---

## Capstone 02 — Review Desk

```mermaid
flowchart TD
  R[Product review text] --> S[sentiment step]
  S --> SUM[summary step]
  SUM --> REP[response step]
  REP --> J[JSON output]
```

Multi-step chain — fixed order, not an agent.

---

## Capstone 03 — Remember-Me Chat

```mermaid
sequenceDiagram
  participant U as User
  participant API as chat function
  participant S as session store
  participant LLM as make_watsonx_llm
  U->>API: message + session_id
  API->>S: load history[session_id]
  S-->>API: prior messages
  API->>LLM: messages + new user turn
  LLM-->>API: reply
  API->>S: save updated history
  API-->>U: response
```

---

## Capstone 04 — Research Agent (ReAct)

```mermaid
flowchart TD
  Q[User question] --> AG[Agent executor]
  AG --> R{ReAct loop}
  R --> T1[search_course_docs tool]
  R --> T2[calculator tool]
  T1 --> R
  T2 --> R
  R --> AN[Final answer]
```

**Not** fixed RAG every time — LLM picks tool from description.

---

## Production pattern (after course)

```mermaid
flowchart LR
  UI[Web / mobile] --> API[FastAPI or Flask]
  API --> ORCH[model.py or chain module]
  ORCH --> LLM[Provider]
  ORCH --> STORE[(session / vector store)]
```

Same separation you built in Module 3: **HTTP thin**, **model utility thick**.