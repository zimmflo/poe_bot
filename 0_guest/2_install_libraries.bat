@echo off
setlocal enabledelayedexpansion

echo Setting up virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Ensuring pip is installed and up-to-date...
python -m ensurepip --default-pip
python -m pip install --upgrade pip setuptools wheel


echo Installing dependencies...
pip install -r requirements.txt
