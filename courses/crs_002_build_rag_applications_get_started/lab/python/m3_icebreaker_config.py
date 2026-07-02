"""Icebreaker lab settings — mirrors 05.pdf config.py (local OpenAI backend)."""

CHUNK_SIZE = 400
SIMILARITY_TOP_K = 5

INITIAL_FACTS_TEMPLATE = """\
You are given LinkedIn profile context below.
Use ONLY this context. Provide three interesting facts about this person's career or education.
Be specific and conversational.

Context:
{context_str}

Facts:
"""

USER_QUESTION_TEMPLATE = """\
You are given LinkedIn profile context below.
Answer the question using ONLY this context.
If the answer is not in the context, say "I don't know."

Context:
{context_str}

Question: {query_str}

Answer:
"""