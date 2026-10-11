@echo off
title Stopping J.A.R.V.I.S.
echo Shutting down JARVIS protocols...
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'jarvis' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
echo All JARVIS processes stopped.
timeout /t 2 >nul
exit
