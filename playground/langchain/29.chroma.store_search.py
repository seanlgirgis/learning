"""Lab 29 — Chroma: store chunk embeddings + similarity_search.

Run set_env.ps1 + network.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\29.chroma.store_search.py
"""

from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from coursera_embeddings import make_embeddings
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
embedding_model = make_embeddings(embed_params)

docsearch = Chroma.from_documents(chunks, embedding_model)
print("Chroma collection ready")

query = "What is LangChain?"
hits = docsearch.similarity_search(query, k=3)
print("Hits:", len(hits))
print("Top hit:", hits[0].page_content[:200])