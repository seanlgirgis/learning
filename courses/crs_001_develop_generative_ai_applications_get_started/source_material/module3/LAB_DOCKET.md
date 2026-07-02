# Module 3 lab docket — Sean’s run log

**Course:** Develop Generative AI Applications: Get Started (Coursera / Skills Network)  
**Lab:** Build Your First GenAI Application The Right Way  
**Started:** 2026-06-19  
**Where this lives:** Cloud IDE → `/home/project`  
**Local mirror:** `lab/python/module3/` + this file

---

## Why we’re doing it this way

Sean hasn’t run this lab before. Foggy on the big LangChain picture is OK — we probe first, tiny scripts second, full Flask app last. No jumping to `app.py` because the PDF says so.

---

## Environment snapshot (2026-06-19 ~17:24 EDT)

| Item | Value |
|------|--------|
| Host | `theia-seangirgis` |
| User | `theia` |
| OS | Linux 6.8.0-117-generic (Ubuntu), x86_64 |
| Project root | `/home/project` |
| Disk | 96G vol, ~42G free on `/home/project` |
| Default Python | **3.10.12** (`/usr/bin/python3`) |
| Lab Python | **3.11.15** available (`/usr/bin/python3.11`) |
| pip (system) | 22.0.2, tied to 3.10 |
| venv | **Not created yet** — `genai_flask_app/venv` pending |
| Pre-installed ML stack | **None** — `pip3 list` had no flask, ibm-watsonx-ai, langchain |

### Env vars (present — values not logged here)

Skills Network already injected watson + other keys. Names we saw:

- `WATSONX_APIKEY`, `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`
- `WATSONX_AI_AUTH_TYPE`, `WATSONX_AI_BEARER_TOKEN`, `WATSONX_TOKEN`
- Also: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `IBM_CLOUD_API_KEY` (toolbox extras)

**Takeaway:** Don’t hardcode API keys. Use `os.environ` — not only `project_id="skills-network"` from the PDF.

---

## Files — local repo (Windows)

Created for copy/paste into Cloud IDE:

| File | Purpose | Status |
|------|---------|--------|
| `lab/python/module3/README.md` | Bite roadmap (Phase 0–2) | Done |
| `lab/python/module3/00_shell_env.sh` | Shell probe | Done |
| `lab/python/module3/00_env_probe.py` | Python + import + env probe | Done |
| `lab/python/module3/01_import_smoke.py` | ibm_watsonx_ai symbol check | Done (not run in cloud yet) |
| `lab/python/module3/02_capital_granite.py` | First LLM call (PDF mirror) | Done — **needs env-var variant for Sean’s IDE** |

---

## Files — Cloud IDE (`/home/project`)

| File | When | Result |
|------|------|--------|
| `00_shell_env.sh` | 2026-06-19 | Ran OK |
| `00_env_probe.py` | 2026-06-19 | Ran OK — all lab imports MISSING (expected) |
| `.theia/` | pre-existing | IDE settings |

**Not in cloud yet:** `genai_flask_app/`, venv, Coursera `capital.py`, `app.py`, etc.

---

## Step log

### Step 0 — Open lab

- Opened Coursera Module 3 guided project in Cloud IDE.
- Left panel = lab instructions; right = Theia/VS Code.
- Terminal: confirmed `pwd` → `/home/project`, `uname` → Linux.

### Step 1 — Shell probe (`00_shell_env.sh`)

- Confirmed python3.11 on PATH (lab PDF says 3.11 venv — we’ll use that).
- Listing: only `.theia` + probe scripts.
- No venv yet — normal.

### Step 2 — Python probe (`00_env_probe.py`)

- Imports: flask, ibm_watsonx_ai, langchain*, pydantic — all missing.
- Env: watson keys **set** — auth should work after `pip install`.
- Challenge: looked “broken” at first glance; actually just **empty venv + no pip installs**.

### Step 3 — venv + ibm-watsonx-ai

- Created venv (python3.11), activated — prompt shows `(venv)`.
- `pip install ibm-watsonx-ai==1.3.39` (assumed — import smoke passed).

### Step 4 — Import smoke (`01_import_smoke.py`)

- **Result:** `ibm_watsonx_ai: Credentials, ModelInference, GenParams — ok`

### Step 5 — First LLM call (`02_capital_granite.py`)

- Sean’s version: env vars for url, apikey, project_id (good).
- **Challenge:** Script exits with **no printed output** (ran twice, blank).
- **Not yet known:** silent empty `generated_text` vs wrong response shape vs URL/region.
- **Next:** Run `02b_capital_debug.py` — prints masked env, full JSON response, `repr(generated_text)`, traceback on error.
- **Local repo:** updated `02_capital_granite.py` + added `02b_capital_debug.py`.

### Step 6 — Debug result (`02b_capital_debug.py`)

- Auth **works** (no exception). `WATSONX_URL` missing → defaulted `us-south`.
- API returned `generated_text: ""` with `generated_token_count: 1`, `stop_reason: eos_token`.
- Warnings: `decoding_method` ignored; **text/generation API deprecated** → use chat API.
- **Hypothesis A:** Coursera PDF uses `Credentials(url=...)` **without** `api_key` — Cloud IDE injects bearer/IAM; explicit api_key may conflict.
- **Hypothesis B:** Granite needs `<|system|>`, `<|user|>`, `<|assistant|>` tokens (lab teaches this later).
- **Fix scripts:** `02c_capital_lab_auth.py` (PDF-style auth), `02d_capital_granite_tokens.py` (tokens + PDF auth).

### Step 7 — Fix confirmed (`02d_capital_granite_tokens.py`)

- **Result:** `'The capital of Canada is Ottawa.'` ✓
- **What fixed it:**
  1. `Credentials(url=...)` only — **no** `api_key` in code (`skills-network` bearer auth).
  2. `project_id="skills-network"` (lab PDF, not only env project id).
  3. Granite tokens: `<|system|>`, `<|user|>`, `<|assistant|>`.
- **Rule for this lab:** Match PDF auth + per-model prompt shape before LangChain wrappers.
- **Next bite:** Llama special tokens (`03_capital_llama_tokens.py`) or skip to `04_langchain_one_model.py` per PDF order.

---

## Pause (2026-06-19) — Flask tutorial first

Sean is new to Flask. **Cloud IDE lab paused** after bite 1 (Granite OK).

**Local path:** `lab/python/flask_tutorial/` — bites 1–3 (hello → json → POST `/generate` stub).

**Resume Module 3 lab when:** Flask bite 3 makes sense; then Cloud IDE LangChain → JSON → plug into `app.py`.

### Flask tutorial local (2026-06-19) — complete

- `01_hello.py` — ran OK
- `02_json_route.py` — JSON + query param + 400/404
- `03_post_echo.py` — POST `/generate` OK; missing `model` → 400 (Sean: “more of an API call” ✓)

### Step 3 — Planned next (superseded)

```bash
mkdir -p genai_flask_app && cd genai_flask_app
python3.11 -m venv venv
source venv/bin/activate
pip install ibm-watsonx-ai==1.3.39
```

Then import smoke → `capital` with env vars.

---

## Challenges & fixes

| Challenge | What happened | Fix / plan |
|-----------|---------------|------------|
| PDF uses `project_id="skills-network"` only | Sean’s IDE has full `WATSONX_*` env | Use `os.environ["WATSONX_APIKEY"]` + `WATSONX_PROJECT_ID` in scripts |
| System python 3.10 vs lab 3.11 | `python3` = 3.10 | Create venv with **`python3.11 -m venv`** |
| No packages on system pip | `pip3 list` minimal | Install **inside venv** after activate |
| Overwhelm / fog | Capstones done but M3 lab new | Investigate → small scripts → full app (this docket) |
| IBM tokens exhausted at home | Playground uses OpenAI shim | **Cloud IDE lab uses real watsonx** — separate from local capstones |

---

## Module 3 quiz notes (same day — Coursera)

Sean checked answers with Grok:

| Q topic | Sean picked | Correct |
|---------|-------------|---------|
| LCEL build order | Wrong order | Define template → PromptTemplate → pipe → invoke |
| Text split why | API cost | **Context window** (+ retrieval chunks) |
| Memory | Read/write continuity | ✓ |
| LCEL pipe syntax | `prompt \| llm \| parser` | ✓ |

Logged in `docs/TRAINING_LOG.md` + RemNote `11-module2-quiz.md`.

---

## Full lab target (from PDF — not started)

End state: Flask app + `config.py` + `model.py` + JSON parser + 3 models (Llama, Granite, Mistral) + `templates/index.html` + static CSS/JS.

Phases left: capital → special tokens → LangChain → JsonOutputParser → Flask → frontend.

---

## Sean reminders

- One bite per terminal session.
- Paste probe output back before next bite.
- This lab ≠ Capstone 04 agent — **you** pick the model; fixed chain each request.
- Local Windows work stays in `D:\Workarea\learning\...`; Cloud IDE is canonical for this lab.

---

### Step 8 — Cloud IDE timeout (2026-06-19)

- Skills Network session timed out; **`/home/project` wiped** (all probe scripts + venv gone).
- **Local mirror intact:** `lab/python/module3/` on Windows — copy/paste from there.
- **Recovery:** venv + `ibm-watsonx-ai` only (skip debug bites 02b/02c unless auth breaks again).
- **Fast path:** import smoke → optional Granite sanity (`02d`) → **Llama 2a/2b** (where we left off).

### Step 9 — Fast recovery (2026-06-19)

- Fresh venv + `ibm-watsonx-ai==1.3.39` — OK.
- `02d_capital_granite_tokens.py` → `'Ottawa'` / `Ottawa` ✓
- `03_capital_llama_plain.py` → messy (echoed prompt + ramble) — **expected**
- `03b_capital_llama_tokens.py` → `The capital of Canada is Ottawa.` ✓
- **Bites 1–2 done.** Next: `04_langchain_one_model.py` (+ langchain packages).

### Step 10 — LangChain pipe (`04_langchain_one_model.py`)

- Pydantic warning: both `WATSONX_API_KEY` and `WATSONX_APIKEY` set — SDK picks one. **Harmless.**
- **Result:** `Ottawa` ✓
- **Bite 3 done.** Next: `05_json_capital_parser.py` (JsonOutputParser → dict).

### Step 11 — JsonOutputParser (`05_json_capital_parser.py`)

- **Result:** `dict {'country': 'Canada', 'capital': 'Ottawa'}` ✓
- **Bite 4 done.** Next: PDF `config.py` + `model.py` + `llm_test.py` (three models).

### Step 12 — llm_test.py (model ID fix)

- **Error:** PDF `llama-3-2-11b-vision-instruct` not in SN supported list.
- **SN allows:** granite-4-h-small, llama-4-maverick-17b-128e-instruct-fp8, mistral-small-3-1-24b-instruct-2503, etc.
- **Fix:** `config.py` → `LLAMA_MODEL_ID = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"` (same as bite 2).

### Step 13 — llm_test.py OK (three models + JSON)

- Llama / Granite / Mistral → `summary`, `sentiment`, `response` ✓
- Sean: `model.py` = utility module; `llm_test` imports model, model imports config.
- **Next:** `app.py` — Flask POST `/generate`.

### Step 14 — app.py + curl tests

- Granite ~0.6s, Llama ~0.6s, Mistral ~1.0s — all return `summary`, `sentiment`, `response`, `duration` ✓
- **Bite 6 done.** Next: `templates/index.html` + `static/` + `render_template` on `/`.

### Step 15 — Full stack verified (no browser preview)

- Running `app2.py` (same as `app.py`).
- **Proof 1:** `curl POST /generate` — granite, llama, mistral → JSON ✓
- **Proof 2:** `curl GET /` → full `index.html` (chat UI markup) ✓
- **Visual GUI:** Coursera “Test your application” / IDE port preview not available or not working — **OK for lab completion**; backend + template path validated on VM.
- **Module 3 guided project:** functionally complete. Mark Coursera steps done; optional: screenshot curl output for notes.

---

*Append to this file each session — files, commands, errors, fixes.*