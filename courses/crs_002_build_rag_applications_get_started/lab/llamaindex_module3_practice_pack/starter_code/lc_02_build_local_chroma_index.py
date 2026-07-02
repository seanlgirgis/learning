"""LangChain step 2: build and persist a local Chroma vector index.

This uses local HuggingFace embeddings, not OpenAI embeddings.
"""

import shutil

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

import lc_config


def main() -> None:
    print("DATA_DIR:", lc_config.DATA_DIR)
    print("PERSIST_DIR:", lc_config.PERSIST_DIR)
    print("LOCAL_EMBEDDING_MODEL:", lc_config.LOCAL_EMBEDDING_MODEL)

    if lc_config.PERSIST_DIR.exists():
        shutil.rmtree(lc_config.PERSIST_DIR)

    loader = DirectoryLoader(
        str(lc_config.DATA_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
    )
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name=lc_config.LOCAL_EMBEDDING_MODEL
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(lc_config.PERSIST_DIR),
        collection_name="company_knowledge",
    )

    print("Documents loaded:", len(documents))
    print("Chunks indexed:", len(chunks))
    print("Vector store persisted at:", lc_config.PERSIST_DIR)

    results = vector_store.similarity_search_with_score(
        "What is the support escalation rule for Sev-1 incidents?",
        k=3,
    )

    print("\nSanity search:")
    for i, (doc, score) in enumerate(results, start=1):
        print("=" * 80)
        print("Rank:", i)
        print("Score:", score)
        print("Source:", doc.metadata.get("source"))
        print(doc.page_content[:500])


if __name__ == "__main__":
    main()
