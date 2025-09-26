@echo off
setlocal

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing build dependencies...
pip install -r requirements.build.txt

echo Creating executable...
pyinstaller app.spec

echo Build completed! Executable is in dist\
pause