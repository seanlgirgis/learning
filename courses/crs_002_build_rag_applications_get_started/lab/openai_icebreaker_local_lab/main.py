"""Command-line Icebreaker Bot — full RAG pipeline in the terminal.

Run from the project folder::

    python main.py --mock

Pipeline (same mental model as Coursera, OpenAI instead of watsonx)::

    extraction → chunks → embeddings → index → query engine → LLM answer → REPL chat

``--mock`` loads ``data/mock_linkedin_profile.json`` (no LinkedIn, no Proxycurl).
OpenAI is used for embeddings and LLM answers after the index is built.
"""

import argparse
import logging
import sys
import time

import bootstrap  # noqa: F401 — puts project root on sys.path
import config
from modules.data_extraction import extract_linkedin_profile
from modules.data_processing import (
    create_vector_database,
    split_profile_data,
    verify_embeddings,
)
from modules.llm_interface import change_llm_model
from modules.query_engine import answer_user_query, generate_initial_facts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout)],
)
logger = logging.getLogger(__name__)


def process_linkedin(
    linkedin_url: str, api_key: str | None = None, mock: bool = False
) -> None:
    """Run the full ingest + icebreaker + chat loop for one profile.

    What it does:
        extraction → split into nodes → embed into index → initial facts → REPL.

    Inputs:
        linkedin_url: Profile URL (placeholder OK when mock=True).
        api_key: Proxycurl key when mock=False.
        mock: If True, read local JSON only (no LinkedIn/Proxycurl).

    Returns:
        None.

    OpenAI:
        Yes — during index build (embeddings) and query steps (LLM).
    """
    try:
        start_time = time.time()

        # Step 1 — extraction (no OpenAI)
        print("Extracting profile data...")
        profile_data = extract_linkedin_profile(
            linkedin_profile_url=linkedin_url, api_key=api_key, mock=mock
        )
        if not profile_data:
            logger.error("Failed to retrieve profile data.")
            return

        # Step 2 — Document → nodes/chunks (no OpenAI)
        print("Splitting profile data into nodes...")
        nodes = split_profile_data(profile_data)
        if not nodes:
            logger.error("Failed to split profile data into nodes.")
            return
        print(f"Created {len(nodes)} node(s).")

        # Step 3 — embeddings → index (OpenAI embeddings)
        print("Creating vector database...")
        vectordb_index = create_vector_database(nodes)
        if not vectordb_index:
            logger.error("Failed to create vector database.")
            return
        if not verify_embeddings(vectordb_index):
            logger.warning("Some embeddings may be missing or invalid.")

        # Step 4 — query engine + LLM (OpenAI LLM)
        print("\nGenerating initial icebreaker facts...")
        initial_facts = generate_initial_facts(vectordb_index)
        print("\nHere are 3 interesting facts about this person:")
        print(initial_facts)
        elapsed = time.time() - start_time
        print(f"\nProfile processed in {elapsed:.2f} seconds.")
        chatbot_interface(vectordb_index)
    except Exception as exc:
        logger.error("Error occurred: %s", exc)


def chatbot_interface(index) -> None:
    """Simple terminal REPL for follow-up profile questions.

    What it does:
        Reads user input in a loop and calls ``answer_user_query`` each turn.

    Inputs:
        index: ``VectorStoreIndex`` built earlier in ``process_linkedin``.

    Returns:
        None (exits on ``exit`` / ``quit`` / ``bye``).

    OpenAI:
        Yes — each question triggers RAG + LLM (unless you exit).
    """
    print("\nYou can now ask more questions about this person.")
    print("Type 'exit', 'quit', or 'bye' to stop.\n")
    while True:
        user_query = input("You: ").strip()
        if user_query.lower() in {"exit", "quit", "bye"}:
            print("Bot: Goodbye!")
            break
        if not user_query:
            continue
        print("Bot is typing...", end="")
        sys.stdout.flush()
        time.sleep(0.5)
        print("\r", end="")
        response = answer_user_query(index, user_query)
        if hasattr(response, "response"):
            print(f"Bot: {response.response.strip()}\n")
        else:
            print(f"Bot: {response}\n")


def main() -> None:
    """Parse CLI flags and start ``process_linkedin``.

    What it does:
        Handles ``--mock``, ``--url``, ``--api-key``, and ``--model`` flags.

    Inputs:
        None (reads ``sys.argv``).

    Returns:
        None.

    OpenAI:
        Indirectly — delegates to ``process_linkedin`` when a profile runs.
    """
    parser = argparse.ArgumentParser(
        description="Local OpenAI Icebreaker Bot - profile RAG assistant"
    )
    parser.add_argument("--url", type=str, help="LinkedIn profile URL")
    parser.add_argument("--api-key", type=str, help="Profile API key")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use local mock data instead of real API data",
    )
    parser.add_argument(
        "--model",
        type=str,
        help='OpenAI LLM model to use, for example "gpt-4o-mini"',
    )
    args = parser.parse_args()
    if args.model:
        change_llm_model(args.model)
    linkedin_url = args.url or ""
    # Default to mock when no URL is provided — safest for learning.
    use_mock = args.mock or not linkedin_url
    if use_mock and not linkedin_url:
        linkedin_url = "https://www.linkedin.com/in/mock-profile/"
    api_key = args.api_key or config.PROXYCURL_API_KEY
    if not use_mock and not api_key:
        api_key = input("Enter API key: ").strip()
    process_linkedin(linkedin_url=linkedin_url, api_key=api_key, mock=use_mock)


if __name__ == "__main__":
    main()