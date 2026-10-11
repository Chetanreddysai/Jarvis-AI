@echo off
title J.A.R.V.I.S. // STARK INDUSTRIES
color 0B
echo ================================================================
echo           STARTING J.A.R.V.I.S. MARK VII SYSTEM
echo ================================================================
echo [1/2] Terminating any old instances...
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'jarvis' -or $_.CommandLine -match 'run_jarvis' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"

cd /d "%~dp0"
echo [2/2] Launching JARVIS Interface & Voice Engine...
python run_jarvis.py
