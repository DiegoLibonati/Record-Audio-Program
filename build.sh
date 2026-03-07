#!/bin/bash
set -e

echo ">>> Activating virtual environment"

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "The virtual environment was not found. Create it with: python -m venv venv"
    exit 1
fi

echo ">>> Installing build dependencies"
pip install -r requirements.build.txt

echo ">>> Creating executable"
pyinstaller app.spec

echo ">>> Build completed! Executable is in dist/"
