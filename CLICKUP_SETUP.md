# ClickUp Setup Guide

## Step 1: Create ClickUp Account

1. Go to https://clickup.com
2. Sign up for free (ClickUp has a generous free tier)
3. Create a workspace (e.g., "Lead Tracker")

## Step 2: Get Your API Token

1. Log in to ClickUp
2. Click your profile picture (bottom left)
3. Click "Settings"
4. Go to "Apps & Integrations" → "API"
5. Click "Generate" to create a personal token
6. Copy the token (keep it secret!)

## Step 3: Find Your Team ID

Option A (via URL):
1. Go to your workspace
2. Look at the URL: `https://app.clickup.com/?team_id=123456789`
3. The number after `team_id=` is your **Team ID**

Option B (via API):
```powershell
$headers = @{
    "Authorization" = "YOUR_API_TOKEN"
}
$response = Invoke-RestMethod -Uri "https://api.clickup.com/api/v2/team" -Headers $headers
$response.teams[0].id
```

## Step 4: Create a List

1. In your workspace, create a new list (or use existing)
2. Name it something like "Lead Follow-ups"
3. Open the list
4. Look at the URL: `https://app.clickup.com/l/li/123456789`
5. The number after `/li/` is your **List ID**

## Step 5: Update .env

In your `.env` file:

```
CLICKUP_API_TOKEN=your_token_here
CLICKUP_TEAM_ID=your_team_id_here
CLICKUP_LIST_ID=your_list_id_here
```

## Step 6: Verify Setup

Run:
```powershell
.\run.ps1 sync
```

The sync should complete without errors. Check ClickUp — you should see tasks created for each lead.

## API Limits

- ClickUp free tier: 100 API calls/minute (plenty for this sync)
- No additional cost

## Troubleshooting

- **"Unauthorized"**: Check your API token
- **"List not found"**: Verify List ID is correct
- **No tasks created**: Check lead status is not "LOST" and sync runs successfully

