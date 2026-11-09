@echo off
title Charisna Visual Agent Desk
cd /d "%~dp0backend"
echo ========================================================
echo [*] Memulai Charisna Visual Agent Desk Backend
echo [*] Akses Web: http://127.0.0.1:19000
echo ========================================================
python app.py
pause
