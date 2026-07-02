"""M3 Step 07b — llm_interface.py workaround (05.pdf Part 5).

Course uses WatsonxEmbeddings / WatsonxLLM — we use OpenAI adapters.

Run:
  python steps/07b_llm_interface_local.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from llama_index.core import Settings

from lib.m3_shared import configure_settings, require_openai


def change_llm_model(model_id: str) -> None:
    """Mirror change_llm_model() — set OPENAI_MODEL then reconfigure."""
    os.environ["OPENAI_MODEL"] = model_id
    configure_settings(temperature=0.0)


def main() -> None:
    require_openai()
    configure_settings(temperature=0.0)

    embed = Settings.embed_model
    llm = Settings.llm
    print("=== create_watsonx_embedding → OpenAIEmbedding ===")
    print(f"embed model: {getattr(embed, 'model_name', embed)}")

    print("\n=== create_watsonx_llm → OpenAI (temperature=0) ===")
    print(f"llm model: {getattr(llm, 'model', llm)}")
    print(f"temperature: {getattr(llm, 'temperature', 'n/a')}")
    print(f"model env: {os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}")

    print("\n=== change_llm_model demo (no API call) ===")
    change_llm_model(os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    print("Model swap = change OPENAI_MODEL in set_env.ps1, then configure_settings().")


if __name__ == "__main__":
    main()