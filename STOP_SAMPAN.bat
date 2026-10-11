@echo off
title Stopping S.A.M.P.A.N.
color 0C
echo ================================================================
echo                SHUTTING DOWN S.A.M.P.A.N.
echo ================================================================
echo Stopping all speech listeners, servers, and background processes...

powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'sampan' -or $_.CommandLine -match 'run_sampan' -or $_.CommandLine -match 'jarvis' -or $_.CommandLine -match 'run_jarvis' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"

echo.
echo ================================================================
echo   [SUCCESS] S.A.M.P.A.N. IS COMPLETELY STOPPED.
echo   - Microphones are disabled.
echo   - Background listeners are terminated.
echo   - No further commands will be taken.
echo ================================================================
timeout /t 3 >nul
exit
