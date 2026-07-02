# Start Jupyter Lab for playground notebooks (custom port — avoids Docker 8888).
param(
    [int]$Port = 8892,
    [switch]$SkipCacheClear
)

$ErrorActionPreference = "Stop"

function Clear-JupyterPlaygroundCaches {
    param(
        [string]$NotebooksRoot
    )

    $removed = 0

    # 1) Notebook autosave checkpoints (main cause of stale cells vs disk)
    $checkpointDir = Join-Path $NotebooksRoot ".ipynb_checkpoints"
    if (Test-Path -LiteralPath $checkpointDir) {
        Remove-Item -LiteralPath $checkpointDir -Recurse -Force
        $removed++
        Write-Host "Cleared: .ipynb_checkpoints" -ForegroundColor Yellow
    }

    # 2) Stale Jupyter server/kernel session files
    $runtimeDir = & jupyter --runtime-dir 2>$null
    if ($runtimeDir -and (Test-Path -LiteralPath $runtimeDir)) {
        Get-ChildItem -LiteralPath $runtimeDir -File -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -match '^(jpserver-|kernel-|nbserver-|jupyterlab-).*\.json$' } |
            ForEach-Object {
                Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue
                $removed++
            }
        if ($removed -gt 0) {
            Write-Host "Cleared: stale files in jupyter runtime" -ForegroundColor Yellow
        }
    }

    # 3) Lab workspace restore (open tabs / unsaved UI state) — optional but helps "fresh open"
    $labWorkspaces = Join-Path $env:APPDATA "jupyter\lab\workspaces"
    if (Test-Path -LiteralPath $labWorkspaces) {
        Remove-Item -LiteralPath $labWorkspaces -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "Cleared: JupyterLab workspace state (tabs/layout reset)" -ForegroundColor Yellow
        $removed++
    }

    if ($removed -eq 0) {
        Write-Host "No Jupyter caches to clear." -ForegroundColor DarkGray
    }
    else {
        Write-Host "Cache clear done. In the browser: close old notebook tabs, then reopen from file tree." -ForegroundColor Green
    }
}

& "D:\py_venv\rag_application_builder_foundation\set_env.ps1"

Set-Location $PSScriptRoot

$langchainDir = Join-Path $PSScriptRoot "..\langchain" | Resolve-Path
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$langchainDir;$env:PYTHONPATH"
}
else {
    $env:PYTHONPATH = "$langchainDir"
}

Write-Host "PYTHONPATH includes: $langchainDir" -ForegroundColor DarkGray
Write-Host ""

if (-not $SkipCacheClear) {
    Clear-JupyterPlaygroundCaches -NotebooksRoot $PSScriptRoot
    Write-Host ""
}

Write-Host "Starting Jupyter Lab on http://127.0.0.1:$Port" -ForegroundColor Cyan
Write-Host "Open: sean_capstone01_ingest_lab.ipynb | sean_langchain_lab.ipynb | sean_in_context_lab.ipynb"
Write-Host "Tip: after git/tool patches, use File -> Reload Notebook from Disk (or reopen tab)."
Write-Host "Skip cache clear next time: .\start_jupyter.ps1 -SkipCacheClear"
Write-Host ""

jupyter lab --port $Port --no-browser --ip 127.0.0.1