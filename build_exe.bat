@echo off
echo 🐍 Snake Game Executable Builder
echo =================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run the build script
echo Building executable...
python build_exe.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo ❌ Build failed! Check the error messages above.
    pause
) else (
    echo.
    echo 🎉 Build completed successfully!
    echo.
    echo The executable is located in: dist\SnakeGame\SnakeGame.exe
    echo.
    echo You can now:
    echo   1. Double-click SnakeGame.exe to run the game
    echo   2. Copy the entire 'dist\SnakeGame' folder to distribute
    echo.
    pause
)
