@echo off
title S.A.M.P.A.N. // AUTONOMOUS AI
color 0B
cd /d "%~dp0"

echo ================================================================
echo           STARTING S.A.M.P.A.N. MARK VII SYSTEM
echo ================================================================
echo Initializing SAMPAN Core & Voice Engine...
python run_sampan.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] S.A.M.P.A.N. exited with code %ERRORLEVEL%.
    pause
)
