"""Extraction smoke test — load mock profile JSON.

OpenAI cost: **NONE** (mock mode only — no LinkedIn, Proxycurl, or OpenAI).

Run::

    python tests/test_data_extraction.py

``mock=True`` reads ``data/mock_linkedin_profile.json``. This is the safest
data-loading check in the test suite.
"""

import setup_imports  # noqa: F401
from modules.data_extraction import extract_linkedin_profile

profile = extract_linkedin_profile(
    linkedin_profile_url="https://www.linkedin.com/in/mock-profile/",
    mock=True,
)
print("Profile loaded:", bool(profile))
print("Top-level keys:", list(profile.keys())[:10])
if profile:
    print(
        "Name:",
        profile.get("full_name") or profile.get("name") or "No name field found",
    )