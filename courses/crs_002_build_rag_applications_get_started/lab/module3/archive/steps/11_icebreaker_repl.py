"""M3 Step 11 — full icebreaker REPL (05.pdf Part 7 main.py).

Run:
  python steps/11_icebreaker_repl.py
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.m3_shared import (
    answer_question,
    build_index_from_profile,
    configure_settings,
    generate_initial_facts,
    load_mock_profile,
    require_openai,
)


def chatbot_interface(index) -> None:
    print("\nAsk about the mock profile. Type exit / quit / bye to stop.\n")
    while True:
        try:
            user_query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break
        if not user_query:
            continue
        if user_query.lower() in {"exit", "quit", "bye"}:
            print("Bot: Goodbye!")
            break
        print(f"Bot: {answer_question(index, user_query)}\n")


def process_linkedin_mock() -> None:
    profile = load_mock_profile()
    print(f"Loaded mock profile: {profile.get('full_name')}")
    index = build_index_from_profile(profile)
    print("\n--- 3 icebreaker facts ---")
    print(generate_initial_facts(index))
    chatbot_interface(index)


def main() -> None:
    require_openai()
    configure_settings()
    process_linkedin_mock()


if __name__ == "__main__":
    main()