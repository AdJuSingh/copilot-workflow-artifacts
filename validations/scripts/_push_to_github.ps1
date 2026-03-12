# Full setup: create GitHub repo + init git + push
param([string]$RepoName = "copilot-workflow-artifacts", [string]$OrgOrUser = "")

$root = 'c:\Users\DGI4KOR\Downloads\copilot-workflow-artifacts-main'

# ── Step 1: Get token via git credential fill ─────────────────────────────
$credInput = "protocol=https`nhost=github.com`n"
$credLines  = ($credInput | git credential fill 2>&1)
$userLine   = $credLines | Where-Object { $_ -match '^username=' }
$passLine   = $credLines | Where-Object { $_ -match '^password=' }
if (-not $passLine) { Write-Host "ERROR: No GitHub credentials found." -ForegroundColor Red; exit 1 }
$token    = ($passLine  -replace '^password=', '').Trim()
$username = ($userLine  -replace '^username=', '').Trim()
Write-Host "Authenticated as: $username" -ForegroundColor Cyan

# ── Step 2: Decide owner ──────────────────────────────────────────────────
$owner = if ($OrgOrUser) { $OrgOrUser } else { $username }

# ── Step 3: Create repo on GitHub via API ─────────────────────────────────
Write-Host "Creating repo: $owner/$RepoName ..." -ForegroundColor Cyan
$headers = @{
    'Authorization' = "Bearer $token"
    'Accept'        = 'application/vnd.github+json'
    'User-Agent'    = 'dashboard-setup'
}
$body = @{ name = $RepoName; description = "Orchestrated AI workflow artifacts for VM domains"; private = $false; auto_init = $false } | ConvertTo-Json
try {
    $created = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType 'application/json' -ErrorAction Stop
    Write-Host ("Repo created: " + $created.html_url) -ForegroundColor Green
    $remoteUrl = $created.clone_url
} catch {
    $msg = $_.ErrorDetails.Message | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($msg.errors -and ($msg.errors | Where-Object { $_.message -match 'already exists' })) {
        Write-Host "Repo already exists, using it." -ForegroundColor Yellow
        $remoteUrl = "https://github.com/$username/$RepoName.git"
    } else {
        Write-Host ("ERROR creating repo: " + $_.Exception.Message) -ForegroundColor Red
        Write-Host $_.ErrorDetails.Message -ForegroundColor Red
        exit 1
    }
}

# ── Step 4: Update _META.repo in workflows.js to match actual owner ────────
$jsPath = Join-Path $root 'docs\dashboard\workflows.js'
$jsContent = [System.IO.File]::ReadAllText($jsPath)
$actualRepo = "$username/$RepoName"
$updated = $jsContent -replace '(?<=repo:\s*")[^"]+', $actualRepo
[System.IO.File]::WriteAllText($jsPath, $updated, [System.Text.Encoding]::UTF8)
Write-Host "Updated _META.repo -> $actualRepo" -ForegroundColor Green

# ── Step 5: Git init, add, commit ─────────────────────────────────────────
Set-Location $root
git init
git config user.email "$username@users.noreply.github.com"
git config user.name  $username
git add .
git commit -m "chore: initial commit — GHCP orchestrated workflow artifacts"

# ── Step 6: Push ──────────────────────────────────────────────────────────
$authenticatedRemote = "https://$username`:$token@github.com/$username/$RepoName.git"
git remote add origin $authenticatedRemote 2>&1 | Out-Null
git branch -M main
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
git push -u origin main
Write-Host ""
Write-Host "Done! Repo live at: https://github.com/$username/$RepoName" -ForegroundColor Green
Write-Host "Next: Actions tab -> '5 . Fetch GitHub Clone Stats' -> Run workflow" -ForegroundColor Yellow
