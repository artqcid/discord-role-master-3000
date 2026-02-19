# Frontend – Discord Role Master 3000
# Dieses Script wird von VS Code Task "Frontend" gestartet

Clear-Host
$width = 50
Write-Host ("=" * $width) -ForegroundColor DarkGray
Write-Host "  *** DISCORD ROLE MASTER 3000 ***" -ForegroundColor Magenta
Write-Host "  Frontend - Vue 3 + Vite Dev Server" -ForegroundColor Magenta
Write-Host ("=" * $width) -ForegroundColor DarkGray
Write-Host ""

$frontendPath = Join-Path $PSScriptRoot "..\frontend"

Write-Host "Checking paths:" -ForegroundColor Gray
Write-Host "Frontend Dir: $frontendPath" -ForegroundColor Gray
Write-Host ""

if (-not (Test-Path $frontendPath)) {
    Write-Host "FEHLER: Frontend-Verzeichnis nicht gefunden!" -ForegroundColor Red
    Write-Host $frontendPath -ForegroundColor Red
    Write-Host "Druecke eine Taste..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "  URL: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "[$( (Get-Date).ToString('HH:mm:ss') )] Starte Vite..." -ForegroundColor Yellow
Write-Host ("-" * $width) -ForegroundColor DarkGray
Write-Host ""

try {
    Set-Location $frontendPath
    npm run dev
    $code = $LASTEXITCODE
    Write-Host ""
    Write-Host ("-" * $width) -ForegroundColor DarkGray
    if ($code -eq 0) {
        Write-Host "[$( (Get-Date).ToString('HH:mm:ss') )] Frontend normal beendet." -ForegroundColor Green
    } else {
        Write-Host "[$( (Get-Date).ToString('HH:mm:ss') )] FEHLER: Exit-Code $code" -ForegroundColor Red
    }
}
catch {
    Write-Host ""
    Write-Host "FEHLER beim Starten des Frontends:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host ""

# Script Ende. Fenster schliessen lassen.

