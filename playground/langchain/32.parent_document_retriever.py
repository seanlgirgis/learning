"""Lab 32 — ParentDocumentRetriever (small search chunks, big context back).

Child chunks (~400 chars) embedded in Chroma; parent chunks (~2000) in InMemoryStore.
Search hits children; retriever returns parents.

Mirror: sean_langchain_lab.ipynb — Parent document retrievers + RetrievalQA prep.

Run set_env.ps1 + network.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\32.parent_document_retriever.py
"""

from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.storage import InMemoryStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter

from coursera_embeddings import make_embeddings

PDF_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "96-FDF8f7coh0ooim7NyEQ/langchain-paper.pdf"
)

document = PyPDFLoader(PDF_URL).load()
print("PDF pages:", len(document))

embed_params = {
    EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
    EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
}
watsonx_embedding = make_embeddings(embed_params)

parent_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=20, separator="\n")
child_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=20, separator="\n")

vectorstore = Chroma(
    collection_name="split_parents",
    embedding_function=watsonx_embedding,
)
store = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

retriever.add_documents(document)
print("Parent IDs in store:", len(list(store.yield_keys())))

sub_docs = vectorstore.similarity_search("Langchain", k=1)
print("Child chunk chars:", len(sub_docs[0].page_content))
print("Child snippet:", sub_docs[0].page_content[:120], "...")

retrieved_docs = retriever.invoke("Langchain")
print("Parent chunk chars:", len(retrieved_docs[0].page_content))
print("Parent snippet:", retrieved_docs[0].page_content[:120], "...")