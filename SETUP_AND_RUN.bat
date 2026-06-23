@echo off
echo ========================================
echo AI Product Chatbot - Setup and Run
echo ========================================
echo.

cd /d "%~dp0backend"

echo Step 1: Installing dependencies...
echo.
python -m pip install google-generativeai
echo.

echo Step 2: Starting the server...
echo.
echo The server will start at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
