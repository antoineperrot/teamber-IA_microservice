@echo off

echo Activating venv
call "%installpath%\Scripts\activate.bat"

echo Running tests
coverage run --source=. -m unittest discover

pause