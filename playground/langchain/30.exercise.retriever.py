"""Lab 30 — Exercise: retriever + multi-query search (notebook twin).

Run set_env.ps1 + network.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\30.exercise.retriever.py
"""

from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from watson_llm import make_watsonx_embeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

WEB_URL = "https://python.langchain.com/v0.2/docs/introduction/"

loader = WebBaseLoader(WEB_URL)
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)
print("Chunks:", len(chunks))

embed_params = {
    EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
    EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
}
embedding_model = make_watsonx_embeddings(embed_params)
vector_store = Chroma.from_documents(chunks, embedding_model)
print("Vector store ready")

retriever = vector_store.as_retriever(search_kwargs={"k": 3})
print("Retriever ready, k=3")


def search_documents(query: str, top_k: int = 3):
    docs = retriever.invoke(query)
    return docs[:top_k]


test_queries = [
    "What is LangChain?",
    "How do retrievers work?",
    "Why is document splitting important?",
]

for query in test_queries:
    print(f"\nQuery: {query}")
    results = search_documents(query)
    print(f"Found {len(results)} relevant documents:")
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}: {doc.page_content[:150]}...")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")