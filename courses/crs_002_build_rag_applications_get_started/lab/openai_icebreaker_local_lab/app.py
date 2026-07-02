"""Gradio web UI for the local OpenAI Icebreaker Bot.

Same RAG pipeline as ``main.py``, wrapped in a browser interface:
Process Profile tab → build index + show icebreaker facts
Chat tab → follow-up questions via query engine

Keep **Use Mock Data** checked while learning — it reads
``data/mock_linkedin_profile.json`` and skips LinkedIn/Proxycurl.
OpenAI tokens are still used for embeddings and LLM answers.
"""

import logging
import sys
import uuid

import gradio as gr

import bootstrap  # noqa: F401
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

# In-memory session store: session_id → VectorStoreIndex (searchable memory).
active_indices = {}


def process_profile(linkedin_url: str, api_key: str, use_mock: bool, selected_model: str):
    """Gradio handler: ingest profile and return icebreaker facts.

    What it does:
        Runs extraction → chunks → index → ``generate_initial_facts``, then
        stores the index under a new session id for the Chat tab.

    Inputs:
        linkedin_url: LinkedIn URL (optional when use_mock=True).
        api_key: Proxycurl key (ignored when use_mock=True).
        use_mock: Load local JSON instead of Proxycurl.
        selected_model: OpenAI LLM id from the dropdown.

    Returns:
        Tuple of (facts text, session_id string).

    OpenAI:
        Yes — embeddings during indexing; LLM for initial facts.
    """
    try:
        if selected_model and selected_model != config.OPENAI_LLM_MODEL:
            change_llm_model(selected_model)
        if use_mock and not linkedin_url:
            linkedin_url = "https://www.linkedin.com/in/mock-profile/"
        profile_data = extract_linkedin_profile(
            linkedin_profile_url=linkedin_url,
            api_key=api_key if not use_mock else None,
            mock=use_mock,
        )
        if not profile_data:
            return "Failed to retrieve profile data.", ""
        nodes = split_profile_data(profile_data)
        if not nodes:
            return "Failed to process profile data into nodes.", ""
        index = create_vector_database(nodes)
        if not index:
            return "Failed to create vector database.", ""
        if not verify_embeddings(index):
            logger.warning("Some embeddings may be missing or invalid.")
        facts = generate_initial_facts(index)
        session_id = str(uuid.uuid4())
        active_indices[session_id] = index
        result = (
            "Profile processed successfully!\n\n"
            "Here are 3 interesting facts about this person:\n\n"
            + facts
        )
        return result, session_id
    except Exception as exc:
        logger.error("Error in process_profile: %s", exc)
        return f"Error: {exc}", ""

def chat_with_profile(session_id: str, user_query: str, chat_history):
    """Chat with a processed profile.

    Gradio's newer Chatbot format expects a list of dictionaries:
    {"role": "user", "content": "..."}
    {"role": "assistant", "content": "..."}
    """
    if chat_history is None:
        chat_history = []

    if not user_query or not user_query.strip():
        return chat_history, ""

    if not session_id:
        chat_history.append(
            {"role": "user", "content": user_query}
        )
        chat_history.append(
            {
                "role": "assistant",
                "content": "No profile loaded. Please process a profile first.",
            }
        )
        return chat_history, ""

    if session_id not in active_indices:
        chat_history.append(
            {"role": "user", "content": user_query}
        )
        chat_history.append(
            {
                "role": "assistant",
                "content": "Session expired. Please process the profile again.",
            }
        )
        return chat_history, ""

    try:
        index = active_indices[session_id]

        response = answer_user_query(index, user_query)

        if hasattr(response, "response"):
            answer_text = response.response
        else:
            answer_text = str(response)

        chat_history.append(
            {"role": "user", "content": user_query}
        )
        chat_history.append(
            {"role": "assistant", "content": answer_text}
        )

        return chat_history, ""

    except Exception as exc:
        logger.error("Error in chat_with_profile: %s", exc)

        chat_history.append(
            {"role": "user", "content": user_query}
        )
        chat_history.append(
            {"role": "assistant", "content": f"Error: {exc}"}
        )

        return chat_history, ""
def create_gradio_interface():
    """Build the Gradio Blocks layout (Process Profile + Chat tabs).

    What it does:
        Wires buttons and textboxes to ``process_profile`` and
        ``chat_with_profile``.

    Inputs:
        None.

    Returns:
        Gradio ``Blocks`` demo object.

    OpenAI:
        No — UI construction only (OpenAI runs when handlers execute).
    """
    available_models = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-4.1"]
    with gr.Blocks(title="Local OpenAI Icebreaker Bot") as demo:
        gr.Markdown("# Local OpenAI Icebreaker Bot")
        gr.Markdown(
            "Generate personalized icebreakers and chat about a LinkedIn/mock profile."
        )
        session_id = gr.Textbox(label="Session ID", visible=False)
        with gr.Tab("Process Profile"):
            with gr.Row():
                with gr.Column():
                    linkedin_url = gr.Textbox(
                        label="LinkedIn Profile URL",
                        placeholder="Leave blank when using mock data",
                    )
                    api_key = gr.Textbox(
                        label="Profile API Key",
                        placeholder="Leave blank when using mock data",
                        type="password",
                        value=config.PROXYCURL_API_KEY,
                    )
                    use_mock = gr.Checkbox(label="Use Mock Data", value=True)
                    model_dropdown = gr.Dropdown(
                        choices=available_models,
                        label="Select OpenAI LLM Model",
                        value=config.OPENAI_LLM_MODEL,
                    )
                    process_btn = gr.Button("Process Profile")
                with gr.Column():
                    result_text = gr.Textbox(label="Initial Facts", lines=14)
            process_btn.click(
                fn=process_profile,
                inputs=[linkedin_url, api_key, use_mock, model_dropdown],
                outputs=[result_text, session_id],
            )
        with gr.Tab("Chat"):
            gr.Markdown("Ask questions about the processed profile.")
            chatbot = gr.Chatbot(height=500)
            chat_input = gr.Textbox(
                label="Ask a question",
                placeholder="What is this person known for?",
            )
            chat_btn = gr.Button("Send")
            chat_btn.click(
                fn=chat_with_profile,
                inputs=[session_id, chat_input, chatbot],
                outputs=[chatbot, chat_input],
            )
            chat_input.submit(
                fn=chat_with_profile,
                inputs=[session_id, chat_input, chatbot],
                outputs=[chatbot, chat_input],
            )
    return demo


if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(server_name="127.0.0.1", server_port=5000, share=False)