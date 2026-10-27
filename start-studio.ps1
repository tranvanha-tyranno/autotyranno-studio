param([switch]$Open)
$ErrorActionPreference = 'Stop'
$studioRoot = $PSScriptRoot
$studioLogs = Join-Path $studioRoot 'data\studio-logs'
New-Item -ItemType Directory -Path $studioLogs -Force | Out-Null
$studioPython = (Get-Command python.exe -ErrorAction Stop).Source
$studioNode = (Get-Command node.exe -ErrorAction Stop).Source
$studioFront = Join-Path $studioRoot 'frontend'
if (-not (Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath $studioPython -ArgumentList @('-m','uvicorn','app.main:app','--app-dir','backend','--host','127.0.0.1','--port','8000') -WorkingDirectory $studioRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $studioLogs 'api.stdout.log') -RedirectStandardError (Join-Path $studioLogs 'api.stderr.log') | Out-Null
}
if (-not (Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue)) {
    $studioNext = Join-Path $studioFront 'node_modules\next\dist\bin\next'
    if (-not (Test-Path -LiteralPath $studioNext)) { throw 'Run npm install in frontend first.' }
    $studioMode = if (Test-Path -LiteralPath (Join-Path $studioFront '.next\BUILD_ID')) { 'start' } else { 'dev' }
    $studioNextArg = '"' + $studioNext + '"'
    Start-Process -FilePath $studioNode -ArgumentList @($studioNextArg,$studioMode,'--hostname','127.0.0.1','--port','3000') -WorkingDirectory $studioFront -WindowStyle Hidden -RedirectStandardOutput (Join-Path $studioLogs 'web.stdout.log') -RedirectStandardError (Join-Path $studioLogs 'web.stderr.log') | Out-Null
}
$studioReady = $false
for ($studioAttempt = 0; $studioAttempt -lt 30; $studioAttempt++) {
    try {
        $studioApi = Invoke-RestMethod 'http://127.0.0.1:8000/health' -TimeoutSec 2
        $studioWeb = Invoke-WebRequest 'http://127.0.0.1:3000' -TimeoutSec 3 -UseBasicParsing
        if ($studioApi.status -eq 'ok' -and $studioWeb.StatusCode -eq 200) { $studioReady = $true; break }
    } catch {}
    Start-Sleep -Milliseconds 500
}
if (-not $studioReady) { throw 'Studio is not ready; check data/studio-logs.' }
Write-Output 'AutoTyranno Studio: http://127.0.0.1:3000'
if ($Open) { Start-Process 'http://127.0.0.1:3000' -WindowStyle Hidden }
