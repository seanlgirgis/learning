"""Environment smoke test — packages, API key visibility, project files.

OpenAI cost: **NONE** (no embedding or LLM API calls).

Run::

    python tests/test_environment.py

Use this first after setup to confirm Python, dependencies, and paths.
"""

import os
import sys
from pathlib import Path

import setup_imports  # noqa: F401
import config


def check(label: str, condition: bool, detail: str = "") -> None:
    """Print one OK/FAIL line for an environment check.

    What it does:
        Formats a single diagnostic result for the console report.

    Inputs:
        label: Short name of the check.
        condition: True means pass.
        detail: Optional extra line printed when provided.

    Returns:
        None.

    OpenAI:
        No.
    """
    status = "OK" if condition else "FAIL"
    print(f"{label}: {status}")
    if detail:
        print(f"  {detail}")


print("=" * 70)
print("ENVIRONMENT CONFIRMATION")
print("=" * 70)

print("\nPython")
print("------")
print("Executable:", sys.executable)
print("Version:", sys.version)
check("Python >= 3.11", sys.version_info >= (3, 11), "Recommended for this lab.")

print("\nPackage imports")
print("---------------")
for package_name in ("llama_index", "openai", "gradio", "dotenv"):
    try:
        __import__(package_name)
        check(f"{package_name} import", True)
    except Exception as exc:
        check(f"{package_name} import", False, str(exc))

print("\nOpenAI configuration")
print("--------------------")
api_key = os.getenv("OPENAI_API_KEY") or config.OPENAI_API_KEY
check(
    "OPENAI_API_KEY visible",
    bool(api_key),
    "Key is configured." if api_key else "Missing. Set it in env or .env.",
)
print("OpenAI LLM model:", config.OPENAI_LLM_MODEL)
print("OpenAI embedding model:", config.OPENAI_EMBEDDING_MODEL)

print("\nProject files")
print("-------------")
mock_path = Path(config.MOCK_DATA_PATH)
check("Mock data file exists", mock_path.exists(), str(mock_path))
check(
    "modules folder exists",
    (setup_imports.PROJECT_ROOT / "modules").exists(),
    str(setup_imports.PROJECT_ROOT / "modules"),
)
check(
    "data folder exists",
    (setup_imports.PROJECT_ROOT / "data").exists(),
    str(setup_imports.PROJECT_ROOT / "data"),
)

print("\nDone.")