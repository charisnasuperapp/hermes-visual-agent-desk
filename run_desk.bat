@echo off
title Hermes Pixel Office — Virtual Agent Desk
cd /d "%~dp0"
echo ========================================================
echo   Hermes Pixel Office (v6.0) — Virtual Agent Desk
echo   Dual-Stack Web Access: http://localhost:8765
echo   Storage Path: %~dp0data
echo ========================================================
timeout /t 1 /nobreak >nul
start http://localhost:8765
python bridge.py
pause
