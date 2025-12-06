# Google Sheets Setup Guide

## Step 1: Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click "Create Project"
3. Enter project name: `automation-two-way-sync`
4. Click "Create"

## Step 2: Enable Google Sheets API

1. Go to https://console.cloud.google.com/apis/dashboard
2. Click "Enable APIs and Services"
3. Search for "Google Sheets API"
4. Click "Enable"
5. Repeat for "Google Drive API" as well

## Step 3: Create Service Account

1. Go to https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click "Create Service Account"
3. Enter name: `automation-sync`
4. Click "Create and Continue"
5. Grant role: **Editor** (for development; restrict in production)
6. Click "Continue"
7. Click "Create Key" → **JSON**
8. A JSON file will download

## Step 4: Save Service Account Key

1. Copy the downloaded JSON file to your project root or safe location
2. Note the file path (you'll need this in `.env`)

## Step 5: Share Google Sheet with Service Account

1. Get the service account email from the JSON file: `client_email`
2. Create a Google Sheet (or use existing one)
3. Click "Share"
4. Paste the service account email
5. Grant **Editor** access
6. Copy the sheet's URL and extract the **Spreadsheet ID**
   - URL example: `https://docs.google.com/spreadsheets/d/ABC123XYZ/edit`
   - Spreadsheet ID: `ABC123XYZ`

## Step 6: Update .env

In your `.automation-two-way-sync/.env` file:

```
GOOGLE_SHEETS_CREDS_JSON=path/to/service-account-key.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_SHEETS_WORKSHEET_NAME=Leads
```

## Step 7: Verify Setup

Run:
```powershell
.\run.ps1 init-sheet
```

You should see headers added to your Google Sheet:
`id, name, email, status, source, task_id`

## Troubleshooting

- **"Permission denied"**: Ensure service account email is shared on the sheet
- **"Spreadsheet not found"**: Double-check Spreadsheet ID
- **"API not enabled"**: Go to Cloud Console and enable Google Sheets API

