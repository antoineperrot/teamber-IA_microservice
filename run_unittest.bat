@echo off
set installpath=%cd%\test_venv
echo Install path : %installpath%

echo Installing test venv
python -m venv "%installpath%"

echo Activating venv
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
