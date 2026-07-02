"""M1 notebook Exercise 2 — return source chunks with the answer.

Run:
  cd D:\\Workarea\\learning\\playground\\langchain
  python ..\\..\\courses\\crs_002_build_rag_applications_get_started\\lab\\python\\05_m1_return_sources.py
"""

from __future__ import annotations

from langchain_classic.chains import RetrievalQA

from m1_rag_shared import POLICIES_URL, build_chroma_from_txt, ensure_text_file, make_llm

QUERY = "what is mobile policy?"


def main() -> None:
    path = ensure_text_file(POLICIES_URL, "companyPolicies.txt")
    docsearch = build_chroma_from_txt(path)
    llm = make_llm()

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )
    result = qa.invoke(QUERY)
    print("Query:", QUERY)
    print("\nAnswer:\n", result.get("result", result))

    sources = result.get("source_documents", [])
    print(f"\nSource chunks returned: {len(sources)}")
    for i, doc in enumerate(sources, 1):
        preview = doc.page_content[:1000].replace("\n", " ")
        print(f"\n--- chunk {i} ---")
        print(preview, "...")


if __name__ == "__main__":
    main()