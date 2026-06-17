"""Lab 23 — Document object (hand-built envelope).

Source material the model can use later — no loader, no network, no watson.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\23.document.object.py
"""

from langchain_core.documents import Document

doc = Document(
    page_content="""Python is an interpreted high-level general-purpose programming language.
Python's design philosophy emphasizes code readability with its notable use of significant indentation.""",
    metadata={
        "my_document_id": 234234,
        "my_document_source": "About Python",
        "my_document_create_time": 1680013019,
    },
)

print("Type:", type(doc))
print("Content:", doc.page_content[:80], "...")
print("Metadata:", doc.metadata)