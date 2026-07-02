"""M3 Step 08 — mock profile load (05.pdf Part 3).

Proxycurl API discontinued → local JSON workaround.

Run:
  python steps/08_mock_profile_load.py
"""

from __future__ import annotations

import json

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.m3_shared import MOCK_PROFILE_PATH, load_mock_profile


def extract_linkedin_profile(url: str, api_key: str, *, mock: bool = True) -> dict:
    """05.pdf Part 3 signature — Proxycurl path kept for reference only."""
    if mock:
        return load_mock_profile()
    _ = (url, api_key)
    raise SystemExit(
        "Proxycurl discontinued Feb 2025. Use mock=True or local JSON at "
        f"{MOCK_PROFILE_PATH}"
    )


def clean_profile(data: dict) -> dict:
    """Same idea as lab: drop empty values."""
    return {k: v for k, v in data.items() if v not in ([], "", None)}


def main() -> None:
    raw = extract_linkedin_profile("https://linkedin.com/in/example", "unused-key", mock=True)
    profile = clean_profile(raw)
    print("Mock profile loaded (local file, not Proxycurl).")
    print(f"  Name: {profile.get('full_name')}")
    print(f"  Headline: {profile.get('headline')}")
    print(f"  Keys: {list(profile.keys())}")
    print("\nSnippet JSON:")
    print(json.dumps({"education": profile.get("education")}, indent=2))


if __name__ == "__main__":
    main()