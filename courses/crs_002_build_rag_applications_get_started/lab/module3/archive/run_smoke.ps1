# Smoke-test Module 3 steps (non-interactive). Step 11 skipped; launch 12 manually.
. D:\py_venv\rag_application_builder_foundation\set_env.ps1
Set-Location $PSScriptRoot

$scripts = @(
    "steps\01_document_class.py",
    "steps\02_simple_directory_reader.py",
    "steps\03_sentence_splitter.py",
    "steps\04_vector_store_index.py",
    "steps\05_as_retriever.py",
    "steps\06_as_query_engine.py",
    "steps\07_prompt_templates.py",
    "steps\07a_test_config.py",
    "steps\07b_llm_interface_local.py",
    "steps\08_mock_profile_load.py",
    "steps\09_profile_split_and_index.py",
    "steps\10_facts_and_qa.py"
)

foreach ($script in $scripts) {
    Write-Host "`n========== $script =========="
    python $script
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED: $script (exit $LASTEXITCODE)"
        exit $LASTEXITCODE
    }
}

Write-Host "`nAll smoke steps passed. Run steps\11_icebreaker_repl.py and steps\12_icebreaker_gradio.py manually."