"""LangChain step 1: load local documents and split them into chunks.

No embeddings.
No LLM.
No provider cost.
"""

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import lc_config


def main() -> None:
    print("DATA_DIR:", lc_config.DATA_DIR)

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

    print("Document count:", len(documents))
    print("Chunk count:", len(chunks))

    if chunks:
        first = chunks[0]
        print("\nFIRST CHUNK TYPE:")
        print(type(first))

        print("\nFIRST CHUNK METADATA:")
        print(first.metadata)

        print("\nFIRST CHUNK PREVIEW:")
        print(first.page_content[:700])


if __name__ == "__main__":
    main()
