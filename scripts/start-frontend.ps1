# Frontend – Discord Role Master 3000
# Dieses Script wird von VS Code Task "Frontend" gestartet

Clear-Host
$width = 50
Write-Host ("=" * $width) -ForegroundColor DarkGray
Write-Host "  *** DISCORD ROLE MASTER 3000 ***" -ForegroundColor Magenta
Write-Host "  Frontend – Vue 3 + Vite Dev Server" -ForegroundColor Magenta
Write-Host ("=" * $width) -ForegroundColor DarkGray
Write-Host ""
Write-Host "  URL: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "[$( (Get-Date).ToString('HH:mm:ss') )] Starte Vite..." -ForegroundColor Yellow
Write-Host ("─" * $width) -ForegroundColor DarkGray
Write-Host ""

$frontendPath = Join-Path $PSScriptRoot "..\..\frontend"

try {
    Set-Location $frontendPath
    npm run dev
    $code = $LASTEXITCODE
    Write-Host ""
    Write-Host ("─" * $width) -ForegroundColor DarkGray
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
Write-Host "  Drücke eine Taste zum Schliessen..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
