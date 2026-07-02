# 01 — Environment Setup

## Goal

Confirm Python, packages, API key, and project files **before** spending OpenAI tokens.

## Setup (PowerShell — shared venv)

```powershell
. D:\py_venv\rag_application_builder_foundation\set_env.ps1
cd D:\Workarea\learning\courses\crs_002_build_rag_applications_get_started\lab\openai_icebreaker_local_lab
pip install -r requirements.txt
```

## Or use a local `.env`

```bash
pip install -r requirements.txt
cp .env.example .env
```

Add `OPENAI_API_KEY=...` to `.env`. Never commit real keys.

## Test (no OpenAI cost)

```bash
python tests/test_environment.py
```

Checks:

- Python version
- `llama_index`, `openai`, `gradio`, `dotenv` imports
- API key visible
- `data/mock_linkedin_profile.json` exists

## Import note

Tests use `tests/setup_imports.py` so `from modules...` works when you run:

```bash
python tests/test_environment.py
```

## Next step

[02_config.md](02_config.md)