@echo off
cd /d "%~dp0backend"
if not exist venv (
  py -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
pause
