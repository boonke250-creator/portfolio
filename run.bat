@echo off
REM Start Flask backend and HTTP server for portfolio

echo Starting Portfolio Admin Dashboard...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt -q

REM Create two terminal windows
start "Flask Backend - http://localhost:5000" cmd /k python app.py
timeout /t 2 /nobreak

start "HTTP Server - http://localhost:8000" cmd /k python -m http.server 8000

echo.
echo ========================================
echo Flask Backend: http://localhost:5000
echo Portfolio: http://localhost:8000/boonke.html
echo Admin: Press Ctrl+Shift+A on the site
echo ========================================
