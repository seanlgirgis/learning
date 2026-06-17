"""Lab 25 — WebBaseLoader (fetch webpage → list of Documents).

Usually one Document for the whole page. Needs network.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\25.loader.web.py
"""

from langchain_community.document_loaders import WebBaseLoader

WEB_URL = "https://python.langchain.com/v0.2/docs/introduction/"

loader = WebBaseLoader(WEB_URL)
web_data = loader.load()

print("Documents loaded:", len(web_data))
print("--- First 1000 chars ---")
print(web_data[0].page_content[:1000])
print("--- Metadata ---")
print(web_data[0].metadata)