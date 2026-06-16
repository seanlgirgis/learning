# start_grok_learning.ps1
# STABLE — do not modify without explicit request from Sean.
#
# Runtime copy (use this):  D:\start_grok_learning.ps1
# Repo archive (git only):  D:\Workarea\learning\start_grok_learning.ps1
# Keep both files identical when a change is ever required.
#
# Location-agnostic launcher: foundation venv -> learning -> Grok Build TUI
#
# Usage (from anywhere):
#   pwsh -ExecutionPolicy Bypass -File "D:\start_grok_learning.ps1"
#
# Opens a new PowerShell window by default. To run in the current shell:
#   ...\start_grok_learning.ps1 -NoNewWindow

param(
    [string]$LearningRoot = 'D:\Workarea\learning',
    [string]$EnvSetter = 'D:\py_venv\rag_application_builder_foundation\set_env.ps1',
    [switch]$NoNewWindow
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$WindowTitle = 'grok_learning'

function Resolve-LearningPaths {
    param(
        [string]$Learning,
        [string]$EnvScript
    )

    if (-not (Test-Path -LiteralPath $Learning)) {
        throw "learning folder not found: $Learning"
    }

    if (-not (Test-Path -LiteralPath $EnvScript)) {
        throw "set_env.ps1 not found: $EnvScript"
    }

    return [ordered]@{
        LearningRoot = (Resolve-Path -LiteralPath $Learning).Path
        EnvSetter    = (Resolve-Path -LiteralPath $EnvScript).Path
    }
}

function Resolve-PwshExecutable {
    $pwshCmd = Get-Command pwsh -ErrorAction SilentlyContinue
    if ($pwshCmd) {
        return $pwshCmd.Source
    }

    $candidates = @(
        (Join-Path $env:ProgramFiles 'PowerShell\7\pwsh.exe')
        (Join-Path $env:ProgramFiles 'PowerShell\6\pwsh.exe')
    )

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    throw "pwsh not found on PATH or under Program Files\PowerShell. Install PowerShell 7+ first."
}

function Resolve-GrokExecutable {
    $grokCmd = Get-Command grok -ErrorAction SilentlyContinue
    if ($grokCmd) {
        return $grokCmd.Source
    }

    $fallback = Join-Path $env:USERPROFILE '.grok\bin\grok.exe'
    if (Test-Path -LiteralPath $fallback) {
        return $fallback
    }

    throw "grok not found on PATH and not at $fallback. Install Grok CLI first."
}

function Get-GrokBootstrapRules {
    @'
For this learning project session:
- Read GROK_AGENTS.md startup order before executing any task.
- Then read GROK_RUNBOOK.md, GROK_CURRENT_STATE.md, and GROK_MEMORY.md as needed.
- Use GROK_ prefix for Grok-specific memory files (GROK_MEMORY.md, GROK_AGENTS.md, GROK_RUNBOOK.md, GROK_CURRENT_STATE.md).
- Full Sean context export: sean_girgis_memory_context_export_2026-06-15.md (confirm time-sensitive facts).
- Run D:\py_venv\rag_application_builder_foundation\set_env.ps1 before any Python commands.
- Sean has ADD/ADHD: keep every response ~1 page or less; one concept at a time; wait for his reply before continuing.
- Focus on small, bite-sized, numbered labs; reusable Python belongs in D:\py_libs\rag_foundation.
- When Sean asks for an opinion, give an honest assessment with tradeoffs — not blind agreement.
'@
}

function Get-GrokBootstrapPrompt {
    param([string]$LearningPath)

    @"
New Grok Build session for learning.

Read GROK_AGENTS.md and follow its startup order before doing any work. Confirm the GROK agent files are loaded and you are operating repository-first in $LearningPath.
"@
}

function Start-GrokLearningSession {
    $paths = Resolve-LearningPaths -Learning $LearningRoot -EnvScript $EnvSetter
    $grokExe = Resolve-GrokExecutable

    try {
        $Host.UI.RawUI.WindowTitle = $WindowTitle
    } catch {
        # Some hosts do not support title changes.
    }

    Write-Host "=== $WindowTitle ===" -ForegroundColor Cyan
    Write-Host "learning: $($paths.LearningRoot)" -ForegroundColor DarkGray

    Write-Host "`nActivating foundation environment..." -ForegroundColor Yellow
    . $paths.EnvSetter

    Set-Location -LiteralPath $paths.LearningRoot
    Write-Host "Working directory: $(Get-Location)" -ForegroundColor Green

    $rules = Get-GrokBootstrapRules
    $prompt = Get-GrokBootstrapPrompt -LearningPath $paths.LearningRoot

    Write-Host "`nStarting Grok Build..." -ForegroundColor Yellow
    & $grokExe --cwd $paths.LearningRoot --rules $rules $prompt
}

if (-not $NoNewWindow) {
    $pwshExe = Resolve-PwshExecutable
    $paths = Resolve-LearningPaths -Learning $LearningRoot -EnvScript $EnvSetter
    $scriptPath = $PSCommandPath

    $argList = @(
        '-NoExit'
        '-ExecutionPolicy', 'Bypass'
        '-File', $scriptPath
        '-LearningRoot', $paths.LearningRoot
        '-EnvSetter', $paths.EnvSetter
        '-NoNewWindow'
    )

    Start-Process -FilePath $pwshExe -ArgumentList $argList -WorkingDirectory $paths.LearningRoot | Out-Null
    return
}

Start-GrokLearningSession