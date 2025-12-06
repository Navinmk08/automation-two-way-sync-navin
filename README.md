automation-two-way-sync
========================

Two-way sync between Google Sheets (Lead Tracker) and ClickUp (Work Tracker).

## Overview
- **Lead Tracker**: Google Sheets (columns: `id,name,email,status,source,task_id`)
- **Work Tracker**: ClickUp list (tasks linked to leads via `task_id` stored in sheet)

This project provides a Python-based sync that:
- ✅ Creates/updates ClickUp tasks for leads in the Google Sheet
- ✅ Updates leads in the sheet when linked ClickUp task statuses change
- ✅ Ensures idempotency (no duplicate tasks)
- ✅ Includes comprehensive error handling and logging
- ✅ Uses retry logic with exponential backoff for reliability

## Status Mapping

**Lead → Task:**
- `NEW` → `To Do`
- `CONTACTED` → `In Progress`
- `QUALIFIED` → `Done`
- `LOST` → (ignored; no task created)

**Task → Lead:**
- Task `Done` → Lead `QUALIFIED`

## Architecture & Flow

```
Google Sheet (Leads) <--> Sync Service <--> ClickUp (Tasks)
```

**Initial Sync Flow:**
1. Read leads from Google Sheet
2. For each lead (status ≠ LOST):
   - If `task_id` is empty, create a ClickUp task and write `task_id` back to sheet
   - Search by `external_id` to avoid duplicates

**Continuous Sync:**
- **Lead → Task**: Lead status change → update linked task status
- **Task → Lead**: Task status = Done → update lead status to QUALIFIED

## Quick Start

### Prerequisites
- Python 3.9+
- Google Cloud account
- ClickUp account
- Git (for repository)

### Setup Steps

1. **Clone or download this project**

2. **Set up Google Sheets** (see [GOOGLE_SHEETS_SETUP.md](./GOOGLE_SHEETS_SETUP.md))
   - Create Google Cloud project
   - Enable Sheets API
   - Create service account
   - Download JSON key
   - Create Google Sheet and share with service account

3. **Set up ClickUp** (see [CLICKUP_SETUP.md](./CLICKUP_SETUP.md))
   - Generate API token
   - Get Team ID
   - Create a List
   - Get List ID

4. **Configure credentials**
   ```powershell
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Install dependencies**
   ```powershell
   .\run.ps1 install
   ```

6. **Initialize sheet**
   ```powershell
   .\run.ps1 init-sheet
   ```

7. **Run the sync**
   ```powershell
   .\run.ps1 sync
   ```

## Running the Sync

```powershell
# One-time sync
.\run.ps1 sync

# Run tests
.\run.ps1 test

# Start FastAPI server (then POST to /sync to trigger)
.\run.ps1 serve

# Health check
curl http://127.0.0.1:8000/health
```

## Project Structure

```
automation-two-way-sync/
├── lead_client.py           # Google Sheets API client
├── task_client.py           # ClickUp API client with retries
├── sync_logic.py            # Two-way sync orchestration
├── config.py                # Environment configuration
├── main.py                  # FastAPI app and CLI entry
├── scripts/
│   └── init_sheet.py        # Initialize sheet headers
├── tests/
│   ├── test_mapping.py      # Status mapping tests
│   └── test_sync_flow.py    # Mock sync flow tests
├── .github/workflows/
│   └── tests.yml            # GitHub Actions CI/CD
├── requirements.txt         # Python dependencies
├── .env.example             # Credentials template
├── SETUP.md                 # Detailed setup guide
├── GOOGLE_SHEETS_SETUP.md   # Step-by-step Google Sheets
├── CLICKUP_SETUP.md         # Step-by-step ClickUp
├── GITHUB_SETUP.md          # Step-by-step GitHub
├── VIDEO_DEMO_GUIDE.md      # Recording instructions
├── COMPLETION_CHECKLIST.md  # Project checklist
└── README.md                # This file
```

## Environment Variables

Copy `.env.example` to `.env` and fill in:

```env
# Google Sheets
GOOGLE_SHEETS_CREDS_JSON=path/to/service-account.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_SHEETS_WORKSHEET_NAME=Leads

# ClickUp
CLICKUP_API_TOKEN=your_api_token
CLICKUP_TEAM_ID=your_team_id
CLICKUP_LIST_ID=your_list_id
```

⚠️ **Never commit `.env` file to Git!** It contains sensitive credentials.

## Error Handling & Idempotency

### Idempotency
- Each created task's ID is stored in the sheet's `task_id` column
- On subsequent runs, sync checks if `task_id` exists before creating new tasks
- Sync searches ClickUp by `external_id` to recover from missed updates
- Result: Safe to run multiple times without creating duplicates

### Error Handling
- All API errors (HTTP status, response) are logged with context
- Per-record exceptions are caught and logged; one bad record doesn't crash sync
- Graceful degradation: partial success is better than total failure

### Retry Logic
- ClickUp client uses exponential backoff (tenacity library)
- Max 3 attempts per API call
- Backoff: 1s → 2s → 4s → 8s

## Limitations & Assumptions

- Google Sheet must have headers: `id,name,email,status,source,task_id` (exact order)
- Only syncs leads with status ≠ `LOST`
- Uses polling (not webhooks) for simplicity
- No advanced field mapping (just basic status sync)
- Demo endpoints have no authentication (add for production)

## Tests

Run all tests:
```powershell
.\run.ps1 test
```

Tests included:
- ✅ Status mapping validation
- ✅ Sync flow with mocks (creates task, updates sheet)
- ✅ Module import checks
- ✅ Syntax validation

## CI/CD

GitHub Actions workflow (`.github/workflows/tests.yml`):
- Runs tests on every push
- Runs daily at 2 AM UTC
- Checks Python syntax

## AI Usage Notes

- **Tools Used**: ChatGPT, GitHub Copilot
- **For What**: README drafting, status mapping logic, code snippets
- **Changes Made**: AI suggested using `external_id` only; I kept `task_id` in sheet for deterministic idempotency and better error recovery
- **Validation**: All code manually reviewed and tested before commit

## Video Demo

🎬 **[Watch the Demo Video](https://drive.google.com/your-link-here)**

The demo shows:
- Setup and credential configuration
- Creating a lead in Google Sheet
- Syncing to ClickUp (task created)
- Updating lead status in Sheet
- Task status updated in ClickUp
- Updating task status in ClickUp
- Lead status updated in Sheet
- Running sync again (idempotency check)

See [VIDEO_DEMO_GUIDE.md](./VIDEO_DEMO_GUIDE.md) for recording instructions.

## Deployment Guide

See [GITHUB_SETUP.md](./GITHUB_SETUP.md) for:
- Creating a GitHub repository
- Pushing code
- Sharing with team members
- GitHub Actions setup

## Troubleshooting

**Import errors?** → Make sure `.env` is configured correctly
**API errors?** → Check credentials in `.env` and verify services are accessible
**No tasks created?** → Verify lead status is not "LOST"
**Sync hangs?** → Check network connection and API rate limits

See individual setup guides for more troubleshooting:
- [GOOGLE_SHEETS_SETUP.md](./GOOGLE_SHEETS_SETUP.md)
- [CLICKUP_SETUP.md](./CLICKUP_SETUP.md)

## Contributing

This is a demo project. To extend:
- Add webhook support (for real-time sync)
- Add more field mapping (custom fields, tags, etc.)
- Add scheduling (APScheduler)
- Add authentication and multi-tenant support

## License

MIT License (or your choice)

## Contact

- Project: automation-two-way-sync
- Repository: [GitHub](https://github.com/YOUR_USERNAME/automation-two-way-sync)
- Used for: drafting README, mapping logic, and small code snippets
- Example change: AI suggested storing ClickUp `external_id` only. I chose to store `task_id` in sheet for reliability and to simplify lookups.

Video Demo
- [Link to demo video on Google Drive](https://drive.google.com/your-video-link-here) — *Upload your video and update this link*
