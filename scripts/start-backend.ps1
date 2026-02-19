# Backend – Discord Role Master 3000
# Dieses Script wird von VS Code Task "Backend" gestartet

Clear-Host
$width = 50
Write-Host ("=" * $width) -ForegroundColor DarkGray
Write-Host "  *** DISCORD ROLE MASTER 3000 ***" -ForegroundColor Cyan
Write-Host "  Backend – FastAPI + Discord Bot" -ForegroundColor Cyan
Write-Host ("=" * $width) -ForegroundColor DarkGray
Write-Host ""
Write-Host "  API:     http://localhost:8000/api" -ForegroundColor White
Write-Host "  Swagger: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "[$( (Get-Date).ToString('HH:mm:ss') )] Starte uvicorn..." -ForegroundColor Yellow
Write-Host ("─" * $width) -ForegroundColor DarkGray
Write-Host ""

try {
    & "$PSScriptRoot\..\..\.venv\Scripts\uvicorn.exe" backend.main:app --reload --port 8000
    $code = $LASTEXITCODE
    Write-Host ""
    Write-Host ("─" * $width) -ForegroundColor DarkGray
    if ($code -eq 0) {
        Write-Host "[$( (Get-Date).ToString('HH:mm:ss') )] Backend normal beendet." -ForegroundColor Green
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
Write-Host "  Drücke eine Taste zum Schliessen..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
