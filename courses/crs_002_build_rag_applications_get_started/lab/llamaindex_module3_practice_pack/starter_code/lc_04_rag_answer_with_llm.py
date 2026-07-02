"""LangChain step 4: local retrieval + LLM answer.

Local embeddings/retrieval.
LLM is used only for final answer writing.
"""

import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

import lc_config


QUESTIONS = [
    "What is the support escalation rule for Sev-1 incidents?",
    "Which product is better for dashboard-style reports?",
    "What changed after the May 2026 analytics outage?",
    "Can I upload API keys into an AI tool?",
    "Who is the CEO of Northwind Analytics?",
]


SYSTEM_PROMPT = """You are a grounded company knowledge-base assistant.

Use only the provided context to answer.
If the answer is not in the context, say it is not specified in the provided context.

Context:
{context}
"""


def format_docs(docs) -> str:
    blocks = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown source")
        blocks.append(f"[Source {i}: {source}]\n{doc.page_content}")
    return "\n\n".join(blocks)


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Run set_env.ps1 first - OPENAI_API_KEY missing.")

    if not lc_config.PERSIST_DIR.exists():
        raise SystemExit(
            "Persisted Chroma index not found. Run lc_02_build_local_chroma_index.py first."
        )

    print("Local embedding model:", lc_config.LOCAL_EMBEDDING_MODEL)
    print("Answer LLM:", lc_config.OPENAI_MODEL)
    print("Vector store:", lc_config.PERSIST_DIR)
    print()

    embeddings = HuggingFaceEmbeddings(
        model_name=lc_config.LOCAL_EMBEDDING_MODEL
    )

    vector_store = Chroma(
        collection_name="company_knowledge",
        persist_directory=str(lc_config.PERSIST_DIR),
        embedding_function=embeddings,
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        model=lc_config.OPENAI_MODEL,
        temperature=lc_config.LLM_TEMPERATURE,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{question}"),
        ]
    )

    for question in QUESTIONS:
        print("=" * 80)
        print("QUESTION:", question)
        print()

        docs = retriever.invoke(question)
        context = format_docs(docs)

        messages = prompt.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        response = llm.invoke(messages)

        print("ANSWER:")
        print(response.content)

        print("\nSOURCES USED:")
        for doc in docs:
            print("-", doc.metadata.get("source"))

        print()


if __name__ == "__main__":
    main()
