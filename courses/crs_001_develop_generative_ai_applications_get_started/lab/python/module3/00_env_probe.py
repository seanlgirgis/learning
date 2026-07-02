"""Module 3 lab — Cloud IDE Python probe (bite 0b).

Run: python3 00_env_probe.py

Does not print secret env values — only whether keys exist.
"""

from __future__ import annotations

import os
import platform
import sys
from pathlib import Path


def _mask_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        return "missing"
    return f"set (len={len(value)})"


def _probe_import(module: str) -> str:
    try:
        __import__(module)
        return "ok"
    except ImportError as exc:
        return f"ImportError: {exc}"


def main() -> None:
    print("=== Cloud IDE Python probe ===")
    print(f"executable: {sys.executable}")
    print(f"version:    {sys.version.split()[0]} ({platform.platform()})")
    print(f"cwd:        {Path.cwd()}")
    print()

    print("--- project files (cwd) ---")
    for entry in sorted(Path.cwd().iterdir()):
        kind = "dir" if entry.is_dir() else "file"
        print(f"  [{kind}] {entry.name}")
    print()

    print("--- imports (lab will need these later) ---")
    for mod in (
        "flask",
        "ibm_watsonx_ai",
        "langchain",
        "langchain_ibm",
        "langchain_core",
        "pydantic",
    ):
        print(f"  {mod}: {_probe_import(mod)}")
    print()

    print("--- watson / skills env (names only, values masked) ---")
    keys = sorted(
        k
        for k in os.environ
        if any(
            part in k.upper()
            for part in ("WATSON", "IBM", "PROJECT", "SKILLS", "API", "TOKEN", "IAM")
        )
    )
    if not keys:
        print("  (no matching env keys — Cloud IDE may inject auth another way)")
    for key in keys:
        print(f"  {key}: {_mask_env(key)}")
    print()

    print("--- pip hints (run manually if imports fail) ---")
    print("  pip3 show ibm-watsonx-ai Flask langchain-ibm langchain")
    print()
    print("Done. Next: python3 01_import_smoke.py")


if __name__ == "__main__":
    main()