@echo off
echo Activating venv
call ".\venv\Scripts\activate.bat"

echo Starting app
call flask --app .\api\servers\base_server.py:app run
pause
