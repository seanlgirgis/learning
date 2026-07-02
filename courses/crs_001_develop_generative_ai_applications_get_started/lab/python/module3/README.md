# Module 3 lab — Cloud IDE bite path

**Coursera lab:** *Build Your First GenAI Application The Right Way*  
**Cloud IDE cwd:** `/home/project` (create `genai_flask_app` when the guide says so)

Copy these files into Cloud IDE, or recreate them line by line. One bite per terminal run.

---

## Phase 0 — Investigate (you are here)

| Bite | Script | What you learn |
|------|--------|----------------|
| 0a | `00_shell_env.sh` | Linux shell, Python on PATH, disk, files in project |
| 0b | `00_env_probe.py` | Python version, imports, watson-related env vars (names only) |
| 0c | `01_import_smoke.py` | Which lab packages import cleanly |

```bash
cd /home/project
bash 00_shell_env.sh
python3 00_env_probe.py
python3 01_import_smoke.py
```

---

## Phase 1 — Small LLM scripts (after probes pass)

| Bite | Script | What you learn |
|------|--------|----------------|
| 1 | `02_capital_granite.py` | Raw `ibm-watsonx-ai` `ModelInference` — one answer |
| 2 | `03_capital_llama_tokens.py` | Same question + Llama special tokens |
| 3 | `04_langchain_one_model.py` | `ChatWatsonx` + `PromptTemplate` + pipe |
| 4 | `05_json_capital_parser.py` | `JsonOutputParser` + Pydantic → Python dict |
| 5 | `genai_flask_app/` config + model + `llm_test.py` | Three models, shared JSON shape |
| 6 | `genai_flask_app/app.py` | Flask POST `/generate` → model handlers |

---

## Phase 2 — Full lab project (Coursera structure)

| Files | Role |
|-------|------|
| `config.py` | Model IDs + GenParams |
| `model.py` | Templates, `JsonOutputParser`, three models |
| `llm_test.py` | Call all models |
| `app.py` | Flask `/generate` |
| `templates/index.html` + `static/` | Web UI |

See `source_material/module3/instructions lab.pdf` for full steps.

---

## Skills Network notes

- Auth is often **pre-wired** (`project_id="skills-network"`) — no API key in your code.
- Lab uses **`python3.11 -m venv venv`** inside `genai_flask_app` — probes in Phase 0 can use system `python3` first.
- If `02_capital_granite.py` fails, re-run `00_env_probe.py` and check watson env + network.

---

## Local mirror (Windows)

Same scripts run on your PC only if `WATSONX_*` env vars are set (`05d_watsonx_smallest_test.py` pattern). Cloud IDE is the canonical run for this lab.

**Run log:** `source_material/module3/LAB_DOCKET.md` — steps, env, files, challenges (updated each session).