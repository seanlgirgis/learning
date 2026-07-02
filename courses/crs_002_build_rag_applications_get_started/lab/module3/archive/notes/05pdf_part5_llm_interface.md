# 05.pdf Part 5 — `llm_interface.py` (local workaround)

Course functions → local equivalent:

| Course (`llm_interface.py`) | Local workaround |
|-----------------------------|------------------|
| `create_watsonx_embedding()` | `lib/m3_shared.configure_settings()` → `OpenAIEmbedding` |
| `create_watsonx_llm(temperature, max_new_tokens, decoding_method)` | `Settings.llm = OpenAI(model=OPENAI_MODEL, temperature=...)` |
| `change_llm_model(new_model_id)` | Change `OPENAI_MODEL` in `set_env.ps1` or env var |

Icebreaker lab params mapped:

| Course param | Local |
|--------------|-------|
| `temperature=0.0` facts | `configure_settings(temperature=0.0)` |
| `decoding_method=greedy` Q&A | OpenAI API default; temperature 0 |
| `max_new_tokens=500` facts | model max_tokens via OpenAI client defaults |

Step script: `steps/07b_llm_interface_local.py` — also wired into steps `04`+ via `m3_shared.configure_settings()`.