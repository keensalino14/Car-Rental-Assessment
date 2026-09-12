@echo off
setlocal
cd /d "%~dp0Car_Rental_System"

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 main.py
    exit /b %errorlevel%
)

where python >nul 2>nul
if %errorlevel%==0 (
    python main.py
    exit /b %errorlevel%
)

echo.
echo Python 3 is required to run Car Rental System.
echo Please install Python 3 from https://www.python.org/downloads/
echo Make sure "Add Python to PATH" is selected during installation.
echo.
pause
