# Stop Backend Script
# Finds python processes running uvicorn and kills them

Write-Host "Stopping Backend (Uvicorn)..." -ForegroundColor Yellow

# 1. Try Graceful Shutdown via API
try {
    Write-Host "Attempting graceful shutdown via API..." -ForegroundColor Cyan
    $response = Invoke-RestMethod -Uri "http://localhost:8001/api/shutdown" -Method Post -ErrorAction Stop -TimeoutSec 3
    Write-Host "Shutdown signal sent. Waiting for process to exit..." -ForegroundColor Green
    Start-Sleep -Seconds 3
} catch {
    Write-Host "Graceful shutdown failed (API not reachable?). Proceeding to force kill." -ForegroundColor DarkGray
}

try {
    # 2. Force Kill leftovers (Watcher process etc.)
    # Find python processes with 'uvicorn' in the command line using WMI/CIM
    $processes = Get-CimInstance Win32_Process | Where-Object { $_.Name -like "*python*" -and $_.CommandLine -like "*uvicorn*" }
    
    if ($processes) {
        foreach ($proc in $processes) {
            Write-Host "Cleaning up process ID: $($proc.ProcessId)" -ForegroundColor Cyan
            Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
        }
        Write-Host "Backend fully stopped." -ForegroundColor Green
    } else {
        if ($response) {
             Write-Host "Backend stopped cleanly." -ForegroundColor Green
        } else {
             Write-Host "No running Backend process found." -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "Error stopping backend: $_" -ForegroundColor Red
    exit 1
}
