@echo off
echo ========================================
echo NetThrottle - Windows Setup
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
echo.

echo Installing required packages...
pip install psutil
pip install tk

echo.
echo Setup complete! You can now run the application using:
echo   run_windows.bat
echo   or
echo   python main.py
echo.
echo Note: Administrator privileges are recommended for optimal performance.
echo.
pause
