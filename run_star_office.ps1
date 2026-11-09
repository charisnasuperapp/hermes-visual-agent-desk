Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "[*] Memulai Star Office UI Backend (ringhyacinth)" -ForegroundColor Green
Write-Host "[*] Akses Web: http://127.0.0.1:19000" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan
Set-Location "$PSScriptRoot\backend"
python app.py
