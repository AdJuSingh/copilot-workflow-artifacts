param([string]$Dir = "")
$dir      = if ($Dir) { $Dir } elseif ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$dashPath = Join-Path $dir "agent-status-dashboard.html"
$jsonPath = Join-Path $dir "workflows.json"

function Sync-Dashboard {
    $json     = Get-Content $jsonPath -Raw -Encoding UTF8
    $html     = Get-Content $dashPath -Raw -Encoding UTF8
    $nl       = [System.Environment]::NewLine
    $newBlock = "<script>" + $nl + "window._WORKFLOWS = " + $json + ";" + $nl + "</script>"
    $pattern  = "(?s)<script>\s*window\._WORKFLOWS\s*=\s*\[[\s\S]*?\];\s*</script>"
    $patched  = $html -replace $pattern, $newBlock
    [System.IO.File]::WriteAllText($dashPath, $patched, [System.Text.Encoding]::UTF8)
    Write-Host ("[" + (Get-Date -Format "HH:mm:ss") + "] Synced -> HTML") -ForegroundColor Green
}

Write-Host "Watcher started. Edit workflows.json and save to auto-sync." -ForegroundColor Cyan
Sync-Dashboard

$watcher                     = New-Object System.IO.FileSystemWatcher
$watcher.Path                = $dir
$watcher.Filter              = "workflows.json"
$watcher.NotifyFilter        = [System.IO.NotifyFilters]::LastWrite
$watcher.EnableRaisingEvents = $true
Write-Host "Watching for changes... (Ctrl+C to stop)" -ForegroundColor DarkCyan

while ($true) {
    $result = $watcher.WaitForChanged([System.IO.WatcherChangeTypes]::Changed, 1000)
    if (-not $result.TimedOut) {
        Start-Sleep -Milliseconds 300
        Sync-Dashboard
    }
}