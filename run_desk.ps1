# Hermes Pixel Office (v6.0) Runner
Set-Location $PSScriptRoot
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Hermes Pixel Office (v6.0) — Virtual Agent Desk" -ForegroundColor Yellow
Write-Host "  Dual-Stack Web Access: http://localhost:8765" -ForegroundColor Green
Write-Host "  Storage Path: $PSScriptRoot\data" -ForegroundColor DarkGray
Write-Host "========================================================" -ForegroundColor Cyan
Start-Process "http://localhost:8765"
python bridge.py
