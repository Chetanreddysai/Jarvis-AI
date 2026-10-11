@echo off
title S.A.M.P.A.N. // BACKGROUND AI
color 0B
cd /d "%~dp0"

echo ================================================================
echo           STARTING S.A.M.P.A.N. BACKGROUND AI
echo ================================================================
echo [1/2] Terminating any previous instances...
python stop_sampan.py >nul 2>&1

echo [2/2] Launching S.A.M.P.A.N. in the background...
start "" pythonw run_background.py

echo.
echo ================================================================
echo   [SUCCESS] S.A.M.P.A.N. IS NOW ACTIVE IN THE BACKGROUND!
echo   - No browser or webpage is opened.
echo   - Microphones are active and listening.
echo   - Just talk to SAMPAN through your laptop microphone anytime!
echo   - Double-click STOP SAMPAN on your Desktop to stop.
echo ================================================================
ping 127.0.0.1 -n 4 >nul
exit
