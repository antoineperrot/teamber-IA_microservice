@echo off
echo Activating venv
call ".\venv\Scripts\activate.bat"

echo Starting app
call python .\api\servers\base_server.py
pause
