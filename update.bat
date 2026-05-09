@echo off
echo Starting Vietnam Stock Data Update...
cd /d %~dp0
C:\Users\ducnx\.venv\Scripts\python.exe src\updater.py
echo Update finished.
pause
