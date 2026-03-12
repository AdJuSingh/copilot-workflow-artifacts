# fetch-clone-stats.ps1
# Fetches real GitHub clone counts and patches docs/dashboard/workflows.js.
#
# Auth strategy (NO manual token creation needed):
#   1. Uses "git credential fill" — reads the GitHub token already stored by
#      VS Code / GitHub Desktop / git for Windows. Completely transparent.
#   2. If git credential fill returns nothing, falls back to Windows Credential
#      Manager key "GHCloneStats" (one-time manual setup, see below).
#
# One-time fallback setup (only if step 1 fails):
#   cmdkey /generic:GHCloneStats /user:github /pass:<YOUR_PAT>
#   (PAT needs: repo → Read-only → Contents + Traffic)

param([string]$WorkspaceRoot = "")

if (-not $WorkspaceRoot) {
    $WorkspaceRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
}
$jsPath = Join-Path $WorkspaceRoot "docs\dashboard\workflows.js"

# ── Step 1: Read repo name from _META in workflows.js ────────────────────────
$jsContent = Get-Content $jsPath -Raw -Encoding UTF8
$repoMatch = [regex]::Match($jsContent, 'repo\s*:\s*"([^"]+)"')
if (-not $repoMatch.Success) {
    Write-Host "ERROR: Could not find repo field in window._META in workflows.js" -ForegroundColor Red
    Write-Host "       Add:  repo: `"owner/repo-name`"  inside window._META = { ... }" -ForegroundColor Yellow
    exit 1
}
$repo = $repoMatch.Groups[1].Value
Write-Host "Repo: $repo" -ForegroundColor Cyan

# ── Step 2: Get auth token via git credential fill ────────────────────────────
$token = $null

# Try git credential fill (uses VS Code / GitHub Desktop stored credentials)
try {
    $credInput = "protocol=https`nhost=github.com`n"
    $credOutput = $credInput | git credential fill 2>$null
    if ($credOutput) {
        $passLine = $credOutput | Where-Object { $_ -match '^password=' }
        if ($passLine) {
            $token = $passLine -replace '^password=', ''
            Write-Host "Auth: Using git credential store (VS Code / git credentials)" -ForegroundColor Green
        }
    }
} catch {}

# Fallback: Windows Credential Manager key "GHCloneStats"
if (-not $token) {
    try {
        $wc = [Windows.Security.Credentials.PasswordVault,Windows.Security.Credentials,ContentType=WindowsRuntime]::new()
        $cred = $wc.Retrieve("GHCloneStats", "github")
        $cred.RetrievePassword()
        $token = $cred.Password
        Write-Host "Auth: Using Windows Credential Manager (GHCloneStats)" -ForegroundColor Green
    } catch {}
}

if (-not $token) {
    Write-Host ""
    Write-Host "No GitHub credentials found. One-time setup required:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Option A — Sign in to GitHub in VS Code:" -ForegroundColor White
    Write-Host "    Open VS Code -> Accounts (bottom-left) -> Sign in with GitHub" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Option B — Store a PAT once in Credential Manager:" -ForegroundColor White
    Write-Host "    1. Create PAT at github.com/settings/tokens (repo -> Contents + Traffic)" -ForegroundColor Gray
    Write-Host "    2. Run: cmdkey /generic:GHCloneStats /user:github /pass:<YOUR_PAT>" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

# ── Step 3: Call GitHub Traffic API ──────────────────────────────────────────
Write-Host "Fetching clone stats from GitHub Traffic API..."
$url     = "https://api.github.com/repos/$repo/traffic/clones"
$headers = @{
    "Authorization" = "Bearer $token"
    "Accept"        = "application/vnd.github+json"
    "User-Agent"    = "dashboard-fetch-clone-stats"
}

try {
    $response = Invoke-RestMethod -Uri $url -Headers $headers -Method Get -ErrorAction Stop
} catch {
    $status = $_.Exception.Response.StatusCode.value__
    if ($status -eq 403 -or $status -eq 404) {
        Write-Host ""
        Write-Host "ERROR: GitHub Traffic API returned $status." -ForegroundColor Red
        Write-Host ""
        Write-Host "The Traffic API requires 'repo' scope — VS Code's OAuth token doesn't include it." -ForegroundColor Yellow
        Write-Host "This is a one-time setup on your machine:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  1. Go to https://github.com/settings/tokens/new" -ForegroundColor White
        Write-Host "     - Note: 'fetch-clone-stats local script'" -ForegroundColor Gray
        Write-Host "     - Expiration: No expiration (or 1 year)" -ForegroundColor Gray
        Write-Host "     - Scope: check 'repo' (gives traffic read access)" -ForegroundColor Gray
        Write-Host "     - Click 'Generate token' and copy it" -ForegroundColor Gray
        Write-Host ""
        Write-Host "  2. Store it once (never enter it again):" -ForegroundColor White
        Write-Host "     cmdkey /generic:GHCloneStats /user:github /pass:<PASTE_TOKEN>" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "  After that, this script picks it up automatically every time." -ForegroundColor Green
        Write-Host ""
        Write-Host "  NOTE: On GitHub, the Actions workflow (5-fetch-clone-stats.yaml)" -ForegroundColor DarkGray
        Write-Host "        runs daily and needs no token — GITHUB_TOKEN has Traffic access." -ForegroundColor DarkGray
    } else {
        Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
    exit 1
}

$count  = $response.count
$unique = $response.uniques
$asOf   = (Get-Date -Format "MMM yyyy")

Write-Host "Clones: $count total, $unique unique (as of $asOf)" -ForegroundColor Green

# ── Step 4: Patch _META in workflows.js ──────────────────────────────────────
$newBlock = "window._META = {`n  repo:   `"$repo`",  // GitHub owner/repo`n  clones: { count: $count, unique: $unique, asOf: `"$asOf`" }`n  // count/unique/asOf are updated automatically -- do not edit by hand`n};"
$patched  = [regex]::Replace($jsContent, 'window\._META\s*=\s*\{[\s\S]*?\};', $newBlock)

[System.IO.File]::WriteAllText($jsPath, $patched, [System.Text.Encoding]::UTF8)
Write-Host "Updated workflows.js -> dashboard will refresh within 5 seconds." -ForegroundColor Green
