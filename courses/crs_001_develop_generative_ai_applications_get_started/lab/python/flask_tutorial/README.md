# Flask tutorial — local (before Module 3 lab)

**Goal:** Understand Flask just enough for the Coursera lab (`app.py`, `/generate`, JSON).

**Not here:** Watson, LangChain, HTML/CSS (lab gives those later).

---

## Setup (once)

```powershell
D:\py_venv\rag_application_builder_foundation\set_env.ps1
cd D:\Workarea\learning\courses\crs_001_develop_generative_ai_applications_get_started\lab\python\flask_tutorial
pip install Flask
```

---

## Bites (run in order)

| Bite | File | You learn |
|------|------|-----------|
| 1 | `01_hello.py` | App, route, `app.run()` |
| 2 | `02_json_route.py` | `jsonify`, GET query params |
| 3 | `03_post_echo.py` | **POST + JSON body** — same shape as lab `/generate` |

Each file: run → open browser or use curl → read code → stop server `Ctrl+C`.

---

## After bite 3

You’ll recognize the lab’s `app.py` skeleton. Return to Cloud IDE Module 3 with `LAB_DOCKET.md` — pick up at LangChain bites, then Flask there.

**Module 3 lab log:** `source_material/module3/LAB_DOCKET.md`