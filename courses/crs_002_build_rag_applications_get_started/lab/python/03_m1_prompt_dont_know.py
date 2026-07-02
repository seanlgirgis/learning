"""M1 notebook — prompt template: say "don't know" when answer not in doc.

Notebook cells ~63–69: query "Can I eat in company vehicles?" is NOT in policies.

Run:
  cd D:\\Workarea\\learning\\playground\\langchain
  python ..\\..\\courses\\crs_002_build_rag_applications_get_started\\lab\\python\\03_m1_prompt_dont_know.py
"""

from __future__ import annotations

from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from m1_rag_shared import POLICIES_URL, build_chroma_from_txt, ensure_text_file, make_llm

QUERY = "Can I eat in company vehicles?"

PROMPT_TEMPLATE = """Use the information from the document to answer the question at the end. If you don't know the answer, just say that you don't know, definately do not try to make up an answer.

{context}

Question: {question}
"""


def main() -> None:
    path = ensure_text_file(POLICIES_URL, "companyPolicies.txt")
    docsearch = build_chroma_from_txt(path)
    llm = make_llm()
    retriever = docsearch.as_retriever()

    print("\n--- Without custom prompt ---")
    qa_plain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
    )
    print("Query:", QUERY)
    print("Answer:", qa_plain.invoke(QUERY))

    print("\n--- With PromptTemplate (notebook pattern) ---")
    prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])
    qa_strict = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False,
    )
    print("Query:", QUERY)
    print("Answer:", qa_strict.invoke(QUERY))


if __name__ == "__main__":
    main()