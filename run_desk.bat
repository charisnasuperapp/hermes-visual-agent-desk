@echo off
title Hermes Visual Agent Desk
cd /d "%~dp0"
echo ========================================================
echo   Hermes Visual Agent Desk - 3D Pixel Garden (HD)
echo   Storage: I:\My Drive\Charisna SuperApp\Hermes\visual_agent_desk\data
echo ========================================================
timeout /t 1 /nobreak >nul
start http://localhost:8765
python bridge.py
pause
