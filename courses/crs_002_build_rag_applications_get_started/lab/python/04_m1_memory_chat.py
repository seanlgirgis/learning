"""M1 notebook — ConversationalRetrievalChain + manual history list.

Notebook cells ~74–88: mobile policy → list points → aim of it (needs "it" = mobile policy).

Run:
  cd D:\\Workarea\\learning\\playground\\langchain
  python ..\\..\\courses\\crs_002_build_rag_applications_get_started\\lab\\python\\04_m1_memory_chat.py
"""

from __future__ import annotations

from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory

from m1_rag_shared import POLICIES_URL, build_chroma_from_txt, ensure_text_file, make_llm

TURNS = [
    "What is mobile policy?",
    "List points in it?",
    "What is the aim of it?",
]


def main() -> None:
    path = ensure_text_file(POLICIES_URL, "companyPolicies.txt")
    docsearch = build_chroma_from_txt(path)
    llm = make_llm()

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=False,
    )

    history: list[tuple[str, str]] = []
    for query in TURNS:
        result = chain.invoke({"question": query, "chat_history": history})
        answer = result["answer"]
        print(f"\nQ: {query}")
        print(f"A: {answer}")
        history.append((query, answer))


if __name__ == "__main__":
    main()