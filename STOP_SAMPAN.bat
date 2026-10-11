@echo off
title Stopping S.A.M.P.A.N.
color 0C
cd /d "%~dp0"
python stop_sampan.py
ping 127.0.0.1 -n 3 >nul
exit
