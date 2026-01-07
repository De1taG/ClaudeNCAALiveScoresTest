@echo off
echo ========================================
echo NCAA Sports Tracker - Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements_desktop.txt

echo.
echo Building executable...
python build_exe.py

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo The executable is located in the 'dist' folder.
echo You can run NCAA_Sports_Tracker.exe from there.
echo.
pause
