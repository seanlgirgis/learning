"""Lab 30 — Exercise: retriever + multi-query search (notebook twin).

Same ingest as Lab 29, then as_retriever() and a small search helper.

Bites (fill together):
  1. Imports
  2. Load web + split → chunks
  3. Chroma.from_documents
  4. retriever = vector_store.as_retriever(search_kwargs={"k": 3})
  5. search_documents(query) helper
  6. Loop test_queries

LangChain 1.x: use retriever.invoke(query) (notebook used get_relevant_documents).

Run set_env.ps1 + network.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\30.exercise.retriever.py
"""

WEB_URL = "https://python.langchain.com/v0.2/docs/introduction/"

# --- Bite 1: imports ---
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from coursera_embeddings import make_embeddings


# --- Bite 2: chunks ---
loader = WebBaseLoader(WEB_URL)
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)
print("Chunks:", len(chunks))


# --- Bite 3: vector store ---
embed_params = {
    EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
    EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
}
embedding_model = make_embeddings(embed_params)

vector_store = Chroma.from_documents(chunks, embedding_model)
print("Vector store ready")


# --- Bite 4: retriever ---
# retriever = vector_store.as_retriever(search_kwargs={"k": 3})
# print("Retriever ready, k=3")


# --- Bite 5: helper ---
# def search_documents(query: str, top_k: int = 3):
#     docs = retriever.invoke(query)
#     return docs[:top_k]


# --- Bite 6: test queries ---
# test_queries = [
#     "What is LangChain?",
#     "How do retrievers work?",
#     "Why is document splitting important?",
# ]
# for query in test_queries:
#     print(f"\nQuery: {query}")
#     results = search_documents(query)
#     print(f"Found {len(results)} relevant documents:")
#     for i, doc in enumerate(results):
#         print(f"\nResult {i+1}: {doc.page_content[:150]}...")
#         print(f"Source: {doc.metadata.get('source', 'Unknown')}")