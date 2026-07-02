#!/usr/bin/env bash
# Module 3 lab — Cloud IDE shell probe (bite 0a)
# Run: bash 00_shell_env.sh

set -e

echo "=== Cloud IDE shell probe ==="
echo "time: $(date -Is 2>/dev/null || date)"
echo

echo "--- identity ---"
pwd
whoami
hostname
uname -a
echo

echo "--- python on PATH ---"
command -v python3 && python3 --version
command -v python3.11 && python3.11 --version || echo "python3.11: not on PATH"
command -v pip3 && pip3 --version || echo "pip3: not on PATH"
echo

echo "--- disk (project folder) ---"
df -h . 2>/dev/null | head -5 || true
echo

echo "--- /home/project listing ---"
ls -la
echo

echo "--- optional: venv if you already created genai_flask_app ---"
if [ -d genai_flask_app/venv ]; then
  echo "found genai_flask_app/venv"
  genai_flask_app/venv/bin/python --version
else
  echo "no genai_flask_app/venv yet (normal on first open)"
fi

echo
echo "Done. Next: python3 00_env_probe.py"