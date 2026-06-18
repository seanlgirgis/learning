# Start Jupyter Lab for playground notebooks (custom port — avoids Docker 8888).
param(
    [int]$Port = 8892
)

$ErrorActionPreference = "Stop"

& "D:\py_venv\rag_application_builder_foundation\set_env.ps1"

Set-Location $PSScriptRoot

$langchainDir = Join-Path $PSScriptRoot "..\langchain" | Resolve-Path
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$langchainDir;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = "$langchainDir"
}

Write-Host "PYTHONPATH includes: $langchainDir" -ForegroundColor DarkGray
Write-Host ""
Write-Host "Starting Jupyter Lab on http://127.0.0.1:$Port" -ForegroundColor Cyan
Write-Host "Open: sean_capstone01_ingest_lab.ipynb | sean_langchain_lab.ipynb | sean_in_context_lab.ipynb"
Write-Host ""

jupyter lab --port $Port --no-browser --ip 127.0.0.1