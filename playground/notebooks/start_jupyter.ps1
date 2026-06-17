# Start Jupyter Lab for playground notebooks (custom port — avoids Docker 8888).
param(
    [int]$Port = 8892
)

$ErrorActionPreference = "Stop"

& "D:\py_venv\rag_application_builder_foundation\set_env.ps1"

Set-Location $PSScriptRoot

Write-Host ""
Write-Host "Starting Jupyter Lab on http://127.0.0.1:$Port" -ForegroundColor Cyan
Write-Host "Open: sean_in_context_lab.ipynb or sean_langchain_lab.ipynb"
Write-Host ""

jupyter lab --port $Port --no-browser --ip 127.0.0.1