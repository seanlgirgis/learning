"""Module 3 lab — import smoke test (bite 0c).

Run: python3 01_import_smoke.py

Confirms the symbols the Coursera lab uses actually load.
"""

from __future__ import annotations


def main() -> None:
    print("=== import smoke ===")

    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

    print("ibm_watsonx_ai: Credentials, ModelInference, GenParams — ok")

    try:
        from langchain_ibm import ChatWatsonx
        print("langchain_ibm: ChatWatsonx — ok")
    except ImportError as exc:
        print(f"langchain_ibm: not yet installed ({exc})")
        print("  lab will: pip install Flask langchain-ibm langchain")

    try:
        from flask import Flask
        print("flask: Flask — ok")
    except ImportError as exc:
        print(f"flask: not yet installed ({exc})")

    try:
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import JsonOutputParser
        from pydantic import BaseModel, Field

        print("langchain_core + pydantic — ok")
    except ImportError as exc:
        print(f"langchain_core/pydantic: ({exc})")

    print()
    print("If ibm-watsonx-ai is ok, next bite: 02_capital_granite.py")


if __name__ == "__main__":
    main()