# Rebuild Gen AI maps in this folder only.
# All maps in the repo: cd Study_bubbles && python tools\studybubble.py rebuild-all
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ids = @(
    "gen_ai_applications_landscape",
    "talk_to_model",
    "prompting",
    "compose_langchain",
    "ground_vectors_chunks",
    "rag_patterns",
    "memory_and_chat",
    "expose_interfaces",
    "agentic"
)

$cli = Join-Path $PSScriptRoot "..\..\Study_bubbles\tools\studybubble.py"
foreach ($id in $ids) {
    Write-Host "Building $id ..." -ForegroundColor Cyan
    python $cli build $id
    if ($LASTEXITCODE -ne 0) { throw "Build failed: $id" }
}

Write-Host ""
Write-Host "Done. Open: outputs\gen_ai_applications_landscape.html" -ForegroundColor Green