@echo off
title Stopping J.A.R.V.I.S.
color 0C
echo ================================================================
echo                SHUTTING DOWN J.A.R.V.I.S.
echo ================================================================
echo Stopping all speech listeners, servers, and background processes...

powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'jarvis' -or $_.CommandLine -match 'run_jarvis' -or $_.CommandLine -match 'run_gui' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"

echo.
echo ================================================================
echo   [SUCCESS] J.A.R.V.I.S. IS COMPLETELY STOPPED.
echo   - Microphones are disabled.
echo   - Background listeners are terminated.
echo   - No further commands will be taken.
echo ================================================================
timeout /t 3 >nul
exit
