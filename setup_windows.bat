@echo off
REM HexaGen GRC Setup Script for Windows
REM This script automates the setup process

echo ========================================
echo HexaGen GRC - Windows Setup
echo ========================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)
python --version
echo Python found!
echo.

REM Check Ollama
echo [2/5] Checking Ollama installation...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Ollama not found!
    echo Please install Ollama from ollama.ai
    echo You can continue without Ollama, but LLM features won't work.
    pause
)
echo.

REM Create virtual environment
echo [3/5] Creating Python virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists!
)
echo.

REM Activate venv and install dependencies
echo [4/5] Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install poetry
poetry install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo Dependencies installed!
echo.

REM Setup environment
echo [5/5] Setting up environment...
if not exist ".env" (
    copy .env.example .env
    echo .env file created! Please edit it with your settings.
) else (
    echo .env file already exists!
)
echo.

REM Initialize directories
echo Initializing HexaGen GRC...
python -m hexagen_grc.cli init
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your settings
echo 2. Install Ollama model: ollama pull mistral:7b-instruct-q4_K_M
echo 3. Activate virtual environment: venv\Scripts\activate.bat
echo 4. Start the server: hexagen serve
echo.
echo For more information, see README.md
echo.
pause
