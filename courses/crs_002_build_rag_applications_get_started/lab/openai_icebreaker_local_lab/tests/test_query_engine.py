"""End-to-end RAG test — embeddings + LLM answers.

OpenAI cost: **YES — embeddings AND LLM** (most expensive test in this folder).

Run only when you explicitly want a full pipeline check::

    python tests/test_query_engine.py

Uses ``mock=True`` for profile data. OpenAI is used for:
    - embedding nodes into the index
    - generating initial facts
    - answering a follow-up question
"""

import setup_imports  # noqa: F401
from modules.data_extraction import extract_linkedin_profile
from modules.data_processing import (
    create_vector_database,
    split_profile_data,
    verify_embeddings,
)
from modules.query_engine import answer_user_query, generate_initial_facts

profile = extract_linkedin_profile(
    linkedin_profile_url="https://www.linkedin.com/in/mock-profile/",
    mock=True,
)
print("Profile loaded:", bool(profile))
nodes = split_profile_data(profile)
print("Nodes created:", len(nodes))
index = create_vector_database(nodes)
print("Index created:", index is not None)
print("Index verified:", verify_embeddings(index) if index else False)
if index:
    print("\nINITIAL FACTS:")
    print(generate_initial_facts(index))
    question = "What is this person known for?"
    print("\nQUESTION:")
    print(question)
    response = answer_user_query(index, question)
    print("\nANSWER:")
    print(response.response if hasattr(response, "response") else response)