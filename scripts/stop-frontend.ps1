# Stop Frontend Script
# Kills all node.exe processes (Standard for this dev environment)

Write-Host "Stopping Frontend (Node)..." -ForegroundColor Yellow

try {
    $processes = Get-Process node -ErrorAction SilentlyContinue
    
    if ($processes) {
        foreach ($proc in $processes) {
            Write-Host "Stopping Node Process ID: $($proc.Id)" -ForegroundColor Cyan
            Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
        }
        Write-Host "Frontend successfully stopped." -ForegroundColor Green
    } else {
        Write-Host "No running Frontend process found." -ForegroundColor Gray
    }
} catch {
    Write-Host "Error stopping frontend: $_" -ForegroundColor Red
    exit 1
}
