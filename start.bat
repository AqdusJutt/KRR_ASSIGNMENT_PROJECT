@echo off
REM Start script for Multi-Agent Chat System (Windows)

echo =========================================
echo Multi-Agent Chat System - Startup
echo =========================================
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file from template...
    python setup_env.py
    echo.
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo =========================================
echo Backend Setup Complete!
echo =========================================
echo.
echo To start the backend server:
echo   uvicorn main:app --reload --port 8000
echo.
echo To start the console client:
echo   python console_client.py
echo.
echo To run tests:
echo   python run_tests.py
echo.
pause

