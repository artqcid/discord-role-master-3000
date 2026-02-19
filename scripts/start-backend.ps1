# Backend – Discord Role Master 3000
# Dieses Script wird von VS Code Task "Backend" gestartet

Clear-Host
$width = 50
Write-Host ("=" * $width) -ForegroundColor DarkGray
Write-Host "  *** DISCORD ROLE MASTER 3000 ***" -ForegroundColor Cyan
Write-Host "  Backend - FastAPI + Discord Bot" -ForegroundColor Cyan
Write-Host ("=" * $width) -ForegroundColor DarkGray
Write-Host ""

# Path Resolution
$venvPath = Join-Path $PSScriptRoot "..\.venv"
$uvicornPath = Join-Path $venvPath "Scripts\uvicorn.exe"

Write-Host "Checking paths:" -ForegroundColor Gray
Write-Host "Script Root: $PSScriptRoot" -ForegroundColor Gray
Write-Host "Venv Path:   $venvPath" -ForegroundColor Gray
Write-Host "Uvicorn:     $uvicornPath" -ForegroundColor Gray
Write-Host ""

if (-not (Test-Path $uvicornPath)) {
    Write-Host "FEHLER: uvicorn.exe nicht gefunden in:" -ForegroundColor Red
    Write-Host $uvicornPath -ForegroundColor Red
    Write-Host "Bitte stelle sicher, dass das Virtual Environment existiert."
    Write-Host "Druecke eine Taste..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "  API:     http://localhost:8000/api" -ForegroundColor White
Write-Host "  Swagger: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "[$( (Get-Date).ToString('HH:mm:ss') )] Starte uvicorn..." -ForegroundColor Yellow
Write-Host ("-" * $width) -ForegroundColor DarkGray
Write-Host ""

try {
Write-Host "Checking for existing instances..." -ForegroundColor Gray
$oldProcs = Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($oldProcs) {
    Write-Host "Killing old instances (PIDs: $oldProcs)..." -ForegroundColor Yellow
    Stop-Process -Id $oldProcs -Force -ErrorAction SilentlyContinue
}

# Nutze python -m uvicorn statt uvicorn.exe direkt
$pythonPath = Join-Path $venvPath "Scripts\python.exe"
& $pythonPath -m uvicorn backend.main:app --reload --port 8001 --host 127.0.0.1
    
    $code = $LASTEXITCODE
    Write-Host ""
    Write-Host ("-" * $width) -ForegroundColor DarkGray
    if ($code -eq 0) {
        Write-Host "[$( (Get-Date).ToString('HH:mm:ss') )] Backend normal beendet." -ForegroundColor Green
    } elseif ($code -eq 1) {
        Write-Host "[$( (Get-Date).ToString('HH:mm:ss') )] Backend wurde gestoppt." -ForegroundColor Yellow
    } else {
        Write-Host "[$( (Get-Date).ToString('HH:mm:ss') )] FEHLER: Exit-Code $code" -ForegroundColor Red
    }
}
catch {
    Write-Host ""
    Write-Host "FEHLER beim Starten des Backends:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host ""

# Script Ende. Fenster schliessen lassen.

