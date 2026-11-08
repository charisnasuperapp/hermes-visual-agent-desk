# Hermes Visual Agent Desk Runner
Set-Location $PSScriptRoot
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Hermes Visual Agent Desk - 3D Pixel Garden (HD)" -ForegroundColor Yellow
Write-Host "  Storage Path: $PSScriptRoot\data" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
Start-Process "http://localhost:8765"
python bridge.py
