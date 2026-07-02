# Play-by-Play Index

Study these in order. Each step matches one module and one test (where noted).

| # | Guide | Module / file | Test | OpenAI cost |
|---|---|---|---|---|
| 0 | [00_big_picture.md](play_by_play/00_big_picture.md) | Overview | — | None |
| 1 | [01_environment_setup.md](play_by_play/01_environment_setup.md) | Setup | `test_environment.py` | None |
| 2 | [02_config.md](play_by_play/02_config.md) | `config.py` | `test_config.py` | None |
| 3 | [03_data_extraction.md](play_by_play/03_data_extraction.md) | `data_extraction.py` | `test_data_extraction.py` | None |
| 4 | [04_llm_interface_openai.md](play_by_play/04_llm_interface_openai.md) | `llm_interface.py` | `test_llm_interface_imports.py` | None |
| 5 | [05_data_processing.md](play_by_play/05_data_processing.md) | `data_processing.py` | `test_data_processing.py` | Embeddings |
| 6 | [06_query_engine.md](play_by_play/06_query_engine.md) | `query_engine.py` | `test_query_engine.py` | Embeddings + LLM |
| 7 | [07_cli_main.md](play_by_play/07_cli_main.md) | `main.py` | `main.py --mock` | Full pipeline |
| 8 | [08_gradio_app.md](play_by_play/08_gradio_app.md) | `app.py` | Browser UI | Full pipeline |
| 9 | [09_troubleshooting.md](play_by_play/09_troubleshooting.md) | Fixes | — | — |

Also read: [OPENAI_VS_WATSONX_MAPPING.md](OPENAI_VS_WATSONX_MAPPING.md)