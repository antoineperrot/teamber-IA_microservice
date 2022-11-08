@echo off
set installpath=%cd%\venv
echo Install path : %installpath%

echo Removing venv if exists
@RD /S /Q "%installpath%"

echo Installing venv
python -m venv "%installpath%"

echo Activating venv
call "%installpath%\Scripts\activate.bat"

echo Installing requirements
call pip install -r requirements.txt

echo Installing dev requirements
call pip install pylint

echo Installing jupyter
call pip install jupyter ipykernel matplotlib pylint

echo Making run_jupyter script and shortcut
echo @echo off> "%installpath%\run_jupyter.bat"
echo call "%installpath%\Scripts\activate.bat">> "%installpath%\run_jupyter.bat"
echo call jupyter notebook>> "%installpath%\run_jupyter.bat"
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%cd%\run_jupyter.lnk');$s.TargetPath='%installpath%\run_jupyter.bat';$s.Save()"

echo Done, start script : %installpath%\run_jupyter.bat
pause
