@echo off
cd /d "%~dp0"
echo Installing google-generativeai...
python -m pip install google-generativeai
echo.
echo Installation complete!
echo.
echo Starting server...
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
