# FlowType Installation Script for Windows

Write-Host "Creating Virtual Environment (using Python 3.9+)..." -ForegroundColor Cyan
py -3.9 -m venv venv

Write-Host "Activating Virtual Environment..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

Write-Host "Installing Dependencies (this may take a minute)..." -ForegroundColor Cyan
.\venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "`nInstallation Complete!" -ForegroundColor Green
Write-Host "To start FlowType, run: " -NoNewline
Write-Host ".\venv\Scripts\python.exe -m src.main" -ForegroundColor Yellow
Write-Host "Make sure you have FFmpeg installed and in your PATH." -ForegroundColor Gray
