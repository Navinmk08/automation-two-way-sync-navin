param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("init-venv", "install", "init-sheet", "sync", "test", "serve")]
    [string]$Command
)

$ErrorActionPreference = "Stop"
$PythonExe = "C:\Users\navin\AppData\Local\Programs\Python\Python314\python.exe"

function Invoke-Init-Venv {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    & $PythonExe -m venv .venv
    Write-Host "Activating venv..." -ForegroundColor Green
    & .\.venv\Scripts\Activate.ps1
}

function Invoke-Install {
    Write-Host "Installing dependencies..." -ForegroundColor Green
    & $PythonExe -m pip install -r requirements.txt
}

function Invoke-Init-Sheet {
    Write-Host "Initializing Google Sheet with headers and sample rows..." -ForegroundColor Green
    & $PythonExe scripts\init_sheet.py
}

function Invoke-Sync {
    Write-Host "Running sync..." -ForegroundColor Green
    & $PythonExe -m main
}

function Invoke-Test {
    Write-Host "Running tests..." -ForegroundColor Green
    & $PythonExe -m pytest -v tests/
}

function Invoke-Serve {
    Write-Host "Starting FastAPI server at http://127.0.0.1:8000" -ForegroundColor Green
    Write-Host "Health: http://127.0.0.1:8000/health" -ForegroundColor Cyan
    Write-Host "Trigger sync: POST http://127.0.0.1:8000/sync" -ForegroundColor Cyan
    & $PythonExe -m uvicorn main:app --reload
}

switch ($Command) {
    "init-venv" { Invoke-Init-Venv }
    "install" { Invoke-Install }
    "init-sheet" { Invoke-Init-Sheet }
    "sync" { Invoke-Sync }
    "test" { Invoke-Test }
    "serve" { Invoke-Serve }
}

Write-Host "Done!" -ForegroundColor Green
