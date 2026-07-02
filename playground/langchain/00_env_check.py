"""Verify playground env without calling any provider API."""

import os
import sys

CHECKS = (
    ("OPENAI_API_KEY", True),
    ("OPENAI_MODEL", False),
    ("OPENAI_EMBEDDING_MODEL", False),
)

print("PLAYGROUND ENV CHECK")
print("=" * 40)

missing_required = []
for name, required in CHECKS:
    value = os.getenv(name)
    if value:
        print(f"  OK   {name} (set)")
    elif required:
        print(f"  MISS {name} (required for provider labs)")
        missing_required.append(name)
    else:
        print(f"  opt  {name} (not set — defaults may apply)")

print()
print("  note  LLM + embeddings use OpenAI (watson_llm stealth swap)")
print()

if missing_required:
    print(
        "Run set_env.ps1 first:\n"
        "  D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1"
    )
    sys.exit(1)

print("Ready for LangChain playground drills.")
print("Next: python .\\01_import_probe.py")