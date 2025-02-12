cd ..
@echo off
python -m venv venv
call venv\Scripts\activate
python -m ensurepip --default-pip
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pause