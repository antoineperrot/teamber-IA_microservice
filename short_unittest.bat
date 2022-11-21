@echo off
echo Activating test_venv
set installpath=%cd%\venv
call "%installpath%\Scripts\activate.bat"

echo Running tests
call python -m unittest discover
coverage run --source=. -m unittest discover

pause