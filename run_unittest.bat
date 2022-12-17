@echo off
set installpath=%cd%\test_venv
echo Install path : %installpath%

echo Removing test_venv if exists
@RD /S /Q "%installpath%"

echo Installing test_venv
python -m test_venv "%installpath%"

echo Activating test_venv
call "%installpath%\Scripts\activate.bat"

echo Installing requirements
call pip install -r requirements.txt

echo Installing coverage
call pip install coverage

echo Running tests
coverage run --source=. -m unittest discover

echo Generating output
coverage html

echo Creating shortcut
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%cd%\coverage.lnk');$s.TargetPath='%cd%\htmlcov\index.html';$s.Save()"

@RD /S /Q "%installpath%"
pause
