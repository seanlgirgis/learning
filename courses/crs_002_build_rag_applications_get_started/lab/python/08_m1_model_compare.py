"""M1 notebook Exercise 3 — compare answers with a second OPENAI_MODEL.

Locally we use OpenAI via watson_llm (not IBM granite/mistral IDs from Coursera).
Run A uses OPENAI_MODEL from set_env.ps1; run B uses MODEL_B below (env override OK).

Run:
  cd D:\\Workarea\\learning\\playground\\langchain
  python ..\\..\\courses\\crs_002_build_rag_applications_get_started\\lab\\python\\08_m1_model_compare.py
"""

from __future__ import annotations

import os

from langchain_classic.chains import RetrievalQA

from m1_rag_shared import POLICIES_URL, build_chroma_from_txt, ensure_text_file, make_llm

QUERY = "what is mobile policy?"

# Run A: OPENAI_MODEL from set_env.ps1 (e.g. gpt-5.4-mini). Run B: this model.
MODEL_B = "gpt-4o"


def ask_with_env_model(model_env_key: str, default: str) -> str:
    model = os.environ.get(model_env_key, default)
    os.environ["OPENAI_MODEL"] = model
    print(f"\n--- OPENAI_MODEL = {model} ---")
    path = ensure_text_file(POLICIES_URL, "companyPolicies.txt")
    docsearch = build_chroma_from_txt(path)
    qa = RetrievalQA.from_chain_type(
        llm=make_llm(),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=False,
    )
    result = qa.invoke(QUERY)
    return str(result.get("result", result))


def main() -> None:
    original = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    model_b = os.environ.get("OPENAI_MODEL_B", MODEL_B)

    print("Query:", QUERY)
    print(f"Model A: {original}  |  Model B: {model_b}")
    a = ask_with_env_model("OPENAI_MODEL", original)
    print("Answer A:", a)

    if model_b == original:
        print("\n(Model B matches A — change MODEL_B in this file or set OPENAI_MODEL_B.)")
    else:
        os.environ["OPENAI_MODEL_B"] = model_b
        b = ask_with_env_model("OPENAI_MODEL_B", model_b)
        print("Answer B:", b)

    os.environ["OPENAI_MODEL"] = original


if __name__ == "__main__":
    main()