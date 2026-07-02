"""Data processing test — split profile, embed chunks, build index.

OpenAI cost: **YES — embeddings only** (``create_vector_database``).

Does NOT call the LLM. Still spends OpenAI embedding tokens.

Run only when you are ready to pay for embeddings::

    python tests/test_data_processing.py

Uses ``mock=True`` for profile loading (no Proxycurl). OpenAI is used when
nodes are embedded into the vector index.
"""

import setup_imports  # noqa: F401
from modules.data_extraction import extract_linkedin_profile
from modules.data_processing import (
    create_vector_database,
    split_profile_data,
    verify_embeddings,
)

profile = extract_linkedin_profile(
    linkedin_profile_url="https://www.linkedin.com/in/mock-profile/",
    mock=True,
)
print("Profile loaded:", bool(profile))
nodes = split_profile_data(profile)
print("Nodes created:", len(nodes))
if nodes:
    print("First node type:", type(nodes[0]).__name__)
    print("First node preview:")
    print(nodes[0].get_content()[:300])
index = create_vector_database(nodes)
print("Index created:", index is not None)
print("Embeddings/index verified:", verify_embeddings(index) if index else False)