@echo off
REM Cinema Management System - Quick Start Script for Windows

echo ================================================
echo  Cinema Management System - Setup Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/6] Installing dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/6] Running migrations...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo.
echo [5/6] Creating superuser...
echo Please enter admin credentials:
python manage.py createsuperuser

if %errorlevel% neq 0 (
    echo NOTE: Superuser creation aborted or failed
)

echo.
echo [6/6] Setup complete!
echo.
echo ================================================
echo  Next Steps:
echo ================================================
echo.
echo To start the development server, run:
echo    python manage.py runserver
echo.
echo Then open your browser and go to:
echo    http://localhost:8000
echo.
echo Admin panel:
echo    http://localhost:8000/admin
echo.
echo To load sample data (optional):
echo    python manage.py shell < seed_data.py
echo.
echo ================================================
echo.
pause
