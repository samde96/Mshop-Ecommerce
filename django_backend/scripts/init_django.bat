@echo off
REM Django Backend Initialization Script for Windows

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo M-Shop Django Backend Setup
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.10+
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please update .env with your configuration
)

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Create superuser
echo Checking for superuser...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(is_superuser=True).exists() or User.objects.create_superuser('admin', 'admin@mshop.local', 'admin123')"

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To start the development server, run:
echo   venv\Scripts\activate.bat
echo   python manage.py runserver 0.0.0.0:8000
echo.
echo To migrate data from MongoDB, run:
echo   python migrate_from_mongodb.py
echo.
echo Access admin at: http://localhost:8000/admin/
echo API at: http://localhost:8000/api/
echo.
pause
