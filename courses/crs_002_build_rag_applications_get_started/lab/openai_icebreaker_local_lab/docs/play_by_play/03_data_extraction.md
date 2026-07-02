# 03 — Data Extraction

**File:** `modules/data_extraction.py`  
**Mental model:** extraction = load profile data

## What this step does

Turns a profile source into a Python dictionary. No chunking, no embeddings, no LLM.

## Mock mode (recommended)

```python
extract_linkedin_profile(..., mock=True)
```

Reads `data/mock_linkedin_profile.json`:

- No LinkedIn website call
- No Proxycurl API call
- No OpenAI

## Live mode (optional)

`mock=False` needs a Proxycurl API key. Still no OpenAI in this file.

## Test (no OpenAI cost)

```bash
python tests/test_data_extraction.py
```

Expect: profile loaded, name printed (Leon Katsnelson in mock data).

## Next step

[04_llm_interface_openai.md](04_llm_interface_openai.md)