param([switch]$OpenAdmin)

$ErrorActionPreference = 'Stop'
$repoPath = Join-Path $PSScriptRoot 'muse2api-czg86389'
$pythonPath = Join-Path $repoPath '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Python environment missing. Create .venv and install requirements.txt first.'
}

$healthUrl = 'http://127.0.0.1:18610/healthz'
$running = $false
try {
    $running = (Invoke-RestMethod -Uri $healthUrl -TimeoutSec 2).status -eq 'ok'
} catch {}

if (-not $running) {
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $dataPath = Join-Path $repoPath 'data'
    New-Item -ItemType Directory -Force -Path $dataPath | Out-Null
    $serviceProcess = Start-Process -FilePath $pythonPath -ArgumentList @(
        '-X', 'utf8', '-m', 'uvicorn', 'app:app',
        '--host', '127.0.0.1', '--port', '18610'
    ) -WorkingDirectory $repoPath -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $dataPath 'server-stdout.log') `
        -RedirectStandardError (Join-Path $dataPath 'server-stderr.log')
    for ($attempt = 0; $attempt -lt 30; $attempt++) {
        try {
            $running = (Invoke-RestMethod -Uri $healthUrl -TimeoutSec 2).status -eq 'ok'
        } catch {}
        if ($running) { break }
        if ($serviceProcess.HasExited) { throw 'Service exited; check data/server-stderr.log.' }
        Start-Sleep -Milliseconds 500
    }
    if (-not $running) { throw 'Service did not become healthy; check data/server-stderr.log.' }
}

Write-Output 'muse2api is running: http://127.0.0.1:18610/admin'
if ($OpenAdmin) {
    $keyLine = Get-Content -LiteralPath (Join-Path $repoPath '.env') |
        Where-Object { $_ -match '^MUSE2API_KEY=' } | Select-Object -First 1
    if (-not $keyLine) { throw 'MUSE2API_KEY is missing from .env.' }
    $localKey = $keyLine.Substring('MUSE2API_KEY='.Length).Trim()
    Start-Process ('http://127.0.0.1:18610/admin?key=' + [uri]::EscapeDataString($localKey)) -WindowStyle Hidden
}
