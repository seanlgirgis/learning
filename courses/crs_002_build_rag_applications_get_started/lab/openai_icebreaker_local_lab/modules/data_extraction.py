"""Load LinkedIn profile data for the Icebreaker RAG pipeline (extraction step).

Mental model — extraction:
    This step loads profile data into a Python dictionary. It does not create
    embeddings, an index, or LLM answers.

Mock mode (recommended for learning):
    mock=True reads ``data/mock_linkedin_profile.json`` locally.
    It does not call LinkedIn or Proxycurl.

Live mode:
    mock=False calls the Proxycurl API with a profile URL and API key.
    Still no OpenAI usage in this file.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import requests

import config

logger = logging.getLogger(__name__)


def extract_linkedin_profile(
    linkedin_profile_url: str,
    api_key: Optional[str] = None,
    mock: bool = False,
) -> Dict[str, Any]:
    """Load profile data from mock JSON or the Proxycurl API.

    What it does:
        Returns a dictionary of profile fields (name, headline, experience, etc.).

    Inputs:
        linkedin_profile_url: LinkedIn URL (ignored when mock=True, but still passed).
        api_key: Proxycurl bearer token. Required when mock=False.
        mock: If True, load ``config.MOCK_DATA_PATH`` instead of calling the API.

    Returns:
        Profile dictionary, or ``{}`` on failure.

    OpenAI:
        No. This step only loads source data.
    """
    try:
        if mock:
            # Local learning path — no network, no API keys needed for profile data.
            logger.info("Using local mock LinkedIn profile data.")
            mock_path = Path(config.MOCK_DATA_PATH)
            with mock_path.open("r", encoding="utf-8") as file:
                return json.load(file)

        if not api_key:
            raise ValueError("API key is required when mock is False.")

        # Live Proxycurl fetch (Coursera lab equivalent — not OpenAI).
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        headers = {"Authorization": f"Bearer {api_key}"}
        params = {
            "url": linkedin_profile_url,
            "fallback_to_cache": "on-error",
            "use_cache": "if-present",
            "skills": "include",
        }
        response = requests.get(
            api_endpoint, headers=headers, params=params, timeout=30
        )
        if response.status_code != 200:
            logger.error(
                "Failed to retrieve data. Status code: %s", response.status_code
            )
            logger.error("Response preview: %s", response.text[:300])
            return {}
        data = response.json()
        # Drop empty fields and noisy LinkedIn extras.
        return {
            k: v
            for k, v in data.items()
            if v not in ([], "", None) and k not in ["people_also_viewed"]
        }
    except Exception as exc:
        logger.error("Error in extract_linkedin_profile: %s", exc)
        return {}