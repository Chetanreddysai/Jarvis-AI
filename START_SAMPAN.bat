@echo off
title S.A.M.P.A.N. // AUTONOMOUS AI
color 0B
echo ================================================================
echo           STARTING S.A.M.P.A.N. MARK VII SYSTEM
echo ================================================================
echo [1/2] Terminating any old instances...
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'sampan' -or $_.CommandLine -match 'run_sampan' -or $_.CommandLine -match 'jarvis' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"

cd /d "%~dp0"
echo [2/2] Launching S.A.M.P.A.N. Interface & Voice Engine...
python run_sampan.py
