# automation-two-way-sync Quick Start

## Setup (first time)

```powershell
# 1. Create and activate virtual environment
.\run.ps1 init-venv

# 2. Install dependencies
.\run.ps1 install

# 3. Copy .env.example to .env and fill in your API keys
cp .env.example .env
# Edit .env with your credentials

# 4. Initialize sheet with headers and sample rows
.\run.ps1 init-sheet
```

## Usage

```powershell
# Run a single sync pass
.\run.ps1 sync

# Run tests
.\run.ps1 test

# Start FastAPI server for on-demand sync
.\run.ps1 serve
# Then POST to http://127.0.0.1:8000/sync
```

## Environment Variables

Copy `.env.example` to `.env` and fill in:
- `GOOGLE_SHEETS_CREDS_JSON` - path to service account JSON
- `GOOGLE_SHEETS_SPREADSHEET_ID` - your sheet ID
- `CLICKUP_API_TOKEN` - your ClickUp token
- `CLICKUP_TEAM_ID` - your ClickUp team ID
- `CLICKUP_LIST_ID` - your ClickUp list ID
