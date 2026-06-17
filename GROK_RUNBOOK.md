# GROK Runbook

Operational procedures for `D:\Workarea\learning`.

## Grok Build Launcher

**Use this to start a session** (opens new window, activates venv, launches Grok Build):

```powershell
pwsh -ExecutionPolicy Bypass -File "D:\start_grok_learning.ps1"
```

| Copy | Path |
|------|------|
| Runtime (daily use) | `D:\start_grok_learning.ps1` |
| Repo archive | `D:\Workarea\learning\start_grok_learning.ps1` |

Keep both copies identical. Run in current shell instead: add `-NoNewWindow`.

## Environment Setup

### Python Virtual Environment

**Always run this before any Python command in this project:**

```powershell
D:\py_venv\rag_application_builder_foundation\set_env.ps1
```

This script activates the correct venv for the learning / RAG application builder foundation stack.

### Verify Activation

After sourcing the script, confirm Python is from the expected venv:

```powershell
D:\py_venv\rag_application_builder_foundation\set_env.ps1
python --version
where.exe python
```

## Common Commands

### New Lab Folder

```powershell
# Example: create lab_01 under a topic folder
New-Item -ItemType Directory -Path "D:\Workarea\learning\rag\lab_01_intro" -Force
```

### Run a Lab Script

```powershell
D:\py_venv\rag_application_builder_foundation\set_env.ps1
python D:\Workarea\learning\rag\lab_01_intro\main.py
```

### Git Status

```powershell
cd D:\Workarea\learning
git status
```

## Related Paths (Outside This Repo)

| Resource | Path |
|----------|------|
| Full memory export | `D:\Workarea\learning\sean_girgis_memory_context_export_2026-06-15.md` |
| Unified course library | `D:\Workarea\StudyBook\study_maps\DataCamp` |
| RAG foundation labs | `...\crs_rag_for_generative_ai_applications\foundation\rag_application_builder_foundation` |
| Shared library | `D:\py_libs\rag_foundation` |

## Folder Layout

Open the hub in a browser: `D:\Workarea\learning\index.html`

```
learning/
├── index.html
├── catalog/         # courses.yaml, units.yaml, paths.yaml
├── courses/         # Coursera (crs_) + DataCamp courses
├── playground/      # Sean-owned drills & experiments (not curriculum)
├── units/           # skills, interview prep, non-course learning
├── paths/           # tracks, certs, custom sequences
├── shared/templates/# HTML study page templates
├── planning/
└── GROK_*.md        # agent session files
```

Labs live inside each course or unit folder (`lab/lab_01_...`). Do not migrate StudyBook content without agreement.

## Troubleshooting

| Issue | Action |
|-------|--------|
| Wrong Python / missing packages | Re-run `set_env.ps1` and verify with `where.exe python` |
| Import errors in a lab | Ensure venv is active; check lab README for extra deps |
| Empty repo | Normal at project start — add labs incrementally |