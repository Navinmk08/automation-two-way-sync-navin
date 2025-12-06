# Setup Instructions

## Prerequisites

You need Python 3.9 or higher. If Python is not installed:

### Option 1: Install Python from python.org (Recommended)
1. Go to https://www.python.org/downloads/
2. Download the latest Python installer (3.11 or 3.12)
3. Run the installer
4. **IMPORTANT**: Check the box "Add Python to PATH" during installation
5. Restart your terminal

### Option 2: Use Windows Package Manager
```powershell
winget install Python.Python.3.12
```

### Option 3: Use Chocolatey (if installed)
```powershell
choco install python
```

## Verify Python Installation

After installing, open a NEW PowerShell terminal and run:
```powershell
python --version
```

You should see: `Python 3.x.x`

## Project Setup

### 1. Create Virtual Environment
```powershell
.\run.ps1 init-venv
```

Or using batch on Command Prompt:
```cmd
run.bat init-venv
```

### 2. Activate Virtual Environment

**PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
.venv\Scripts\activate.bat
```

### 3. Install Dependencies
```powershell
.\run.ps1 install
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env`:
```powershell
cp .env.example .env
```

Edit `.env` and fill in:
- `GOOGLE_SHEETS_CREDS_JSON` - Path to service account JSON key
- `GOOGLE_SHEETS_SPREADSHEET_ID` - Your spreadsheet ID
- `CLICKUP_API_TOKEN` - Your ClickUp API token
- `CLICKUP_TEAM_ID` - Your ClickUp team ID
- `CLICKUP_LIST_ID` - Your ClickUp list ID

### 5. Initialize Google Sheet (Optional)
```powershell
.\run.ps1 init-sheet
```

This creates the headers and sample rows in your sheet.

## Running the Sync

### One-Time Sync
```powershell
.\run.ps1 sync
```

### Run Tests
```powershell
.\run.ps1 test
```

### Start API Server
```powershell
.\run.ps1 serve
```

Then POST to `http://127.0.0.1:8000/sync` to trigger the sync.

## Troubleshooting

### "python: command not found"
- Restart your terminal after installing Python
- Make sure Python is added to PATH
- Try using `python.exe` instead of `python`

### venv activation fails
- Make sure you're using the correct activation script for your shell
- Use `.venv\Scripts\Activate.ps1` for PowerShell
- Use `.venv\Scripts\activate.bat` for Command Prompt

### "ModuleNotFoundError"
- Make sure venv is activated (you should see `(.venv)` in your prompt)
- Run `pip install -r requirements.txt` again

### API errors
- Check your `.env` file has correct credentials
- Verify service account has access to the Google Sheet
- Verify ClickUp token and list ID are correct
