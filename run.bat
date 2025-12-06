@echo off
REM Windows batch script for common commands using Python 3.14
REM Usage: run.bat init-venv | run.bat install | run.bat sync | etc.

set PYTHON_EXE=C:\Users\navin\AppData\Local\Programs\Python\Python314\python.exe

if "%1"=="" (
    echo Usage: run.bat [command]
    echo Commands:
    echo   init-venv   - Create virtual environment
    echo   install     - Install dependencies
    echo   init-sheet  - Initialize Google Sheet
    echo   sync        - Run sync once
    echo   test        - Run tests
    echo   serve       - Start FastAPI server
    exit /b 1
)

if "%1"=="init-venv" (
    echo Creating virtual environment...
    %PYTHON_EXE% -m venv .venv
    call .venv\Scripts\activate.bat
    goto end
)

if "%1"=="install" (
    echo Installing dependencies...
    %PYTHON_EXE% -m pip install -r requirements.txt
    goto end
)

if "%1"=="init-sheet" (
    echo Initializing Google Sheet...
    %PYTHON_EXE% scripts\init_sheet.py
    goto end
)

if "%1"=="sync" (
    echo Running sync...
    %PYTHON_EXE% -m main
    goto end
)

if "%1"=="test" (
    echo Running tests...
    %PYTHON_EXE% -m pytest -v tests/
    goto end
)

if "%1"=="serve" (
    echo Starting FastAPI server at http://127.0.0.1:8000
    echo Health: http://127.0.0.1:8000/health
    echo Trigger sync: POST http://127.0.0.1:8000/sync
    %PYTHON_EXE% -m uvicorn main:app --reload
    goto end
)

echo Unknown command: %1
exit /b 1

:end
echo Done!
