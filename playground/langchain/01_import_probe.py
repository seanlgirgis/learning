"""Test which Coursera-lab imports work in the foundation venv (LangChain 1.x)."""

import importlib
import sys

# (label, import statement, coursera_notebook_import_if_different)
IMPORTS = [
    (
        "langchain_core prompts",
        "from langchain_core.prompts import PromptTemplate, ChatPromptTemplate",
        None,
    ),
    (
        "langchain_core parsers",
        "from langchain_core.output_parsers import StrOutputParser",
        None,
    ),
    (
        "langchain_core runnables",
        "from langchain_core.runnables import RunnablePassthrough",
        None,
    ),
    (
        "langchain_core messages",
        "from langchain_core.messages import HumanMessage, SystemMessage",
        None,
    ),
    (
        "langchain_ibm",
        "from langchain_ibm import WatsonxLLM",
        None,
    ),
    (
        "ibm_watsonx_ai",
        "from ibm_watsonx_ai.metanames import GenTextParamsMetaNames",
        None,
    ),
    (
        "LLMChain (classic)",
        "from langchain_classic.chains import LLMChain",
        "Coursera: from langchain.chains import LLMChain",
    ),
    (
        "SequentialChain (classic)",
        "from langchain_classic.chains import SequentialChain",
        "Coursera: from langchain.chains import SequentialChain",
    ),
    (
        "ConversationBufferMemory (classic)",
        "from langchain_classic.memory import ConversationBufferMemory",
        "Coursera: from langchain.memory import ConversationBufferMemory",
    ),
]

print("IMPORT PROBE — foundation venv")
print("=" * 50)

failed = 0
for label, statement, note in IMPORTS:
    try:
        exec(statement, {})
        print(f"  OK   {label}")
        if note:
            print(f"       {note}")
    except Exception as error:
        failed += 1
        print(f"  FAIL {label}: {error}")
        if note:
            print(f"       Use instead: {statement}")

print()
if failed:
    print(
        "Some imports failed. For LLMChain / memory, install:\n"
        "  pip install langchain-classic"
    )
    sys.exit(1)

print("All playground imports available.")
print()
print("Coursera notebooks pin langchain 0.2.x; this venv uses 1.x.")
print("See coursera_import_map.md for copy-paste fixes in notebook cells.")