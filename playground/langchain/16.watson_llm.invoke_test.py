"""Lab 16 — test watson_llm (WatsonxLLM from WATSONX_* env).

Like the LangChain notebook Chat model cells:
    from watson_llm import make_watsonx_llm
    llama_llm = make_watsonx_llm()
    print(llama_llm.invoke("Who is man's best friend?"))

Run:
    D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\16.watson_llm.invoke_test.py
"""

import os

from watson_llm import make_watsonx_llm


def main() -> None:
    print("Loaded watson_llm.py")
    print("Model:", os.environ.get("OPENAI_MODEL", "gpt-4o-mini"))
    print()

    llama_llm = make_watsonx_llm()  # OpenAI via watson_llm stealth shim
    print(llama_llm.invoke("Who is man's best friend?"))


if __name__ == "__main__":
    main()