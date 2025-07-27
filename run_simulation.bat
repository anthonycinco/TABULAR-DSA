@echo off
REM RF Learning System - Simulation Runner
REM This script runs the RF Learning System in simulation mode

echo RF Learning System - Simulation Mode
echo ======================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist rf_learning_env\Scripts\activate.bat (
    echo Activating virtual environment...
    call rf_learning_env\Scripts\activate.bat
) else (
    echo Virtual environment not found. Using system Python.
)

echo.
echo Starting RF Learning System in simulation mode...
echo This will run 50 episodes to demonstrate the system.
echo.
echo Press Ctrl+C to stop early.
echo.

python main_system.py --simulate --episodes 50

echo.
echo Simulation completed!
echo Check the generated files:
echo - final_results.png (performance plots)
echo - channel_heatmap.png (channel usage analysis)
echo - q_table.pkl (learned Q-table)
echo - system_log.txt (detailed logs)
echo.

pause 