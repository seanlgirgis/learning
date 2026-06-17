"""Lab 16 — test langchain_helper (WatsonxLLM from WATSONX_* env).

Like the LangChain notebook Chat model cells:
    from coursera_llm_model import make_llm
    llama_llm = make_llm()
    print(llama_llm.invoke("Who is man's best friend?"))

Run:
    D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\16.langchain_helper.invoke_test.py
"""

import os

from langchain_helper import make_llm


def main() -> None:
    print("Loaded langchain_helper.py")
    print("Model:", os.environ["WATSONX_MODEL_ID"])
    print()

    llama_llm = make_llm()  # WatsonxLLM — name kept like the notebook
    print(llama_llm.invoke("Who is man's best friend?"))


if __name__ == "__main__":
    main()