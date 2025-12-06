# Video Demo Guide

## What to Record

Record a screen capture video (max 10 minutes) showing:

### 1. Introduction (1 min)
- Brief intro: "This is a two-way sync between Google Sheets and ClickUp"
- Show tools: Google Sheets tab, ClickUp tab
- Mention: Data stays in sync automatically

### 2. Setup & Configuration (2 min)
- Show `.env.example` being copied to `.env`
- Show `.env` with credentials filled in (REDACT tokens/keys)
- Show running: `.\run.ps1 init-sheet`
- Verify headers in Google Sheet

### 3. Initial Sync Demo (2 min)
- Create a new lead in Google Sheet manually
  - Example: "Acme Corp", "contact@acme.com", status "NEW"
- Run: `.\run.ps1 sync`
- Show the task automatically created in ClickUp
- Verify task title includes the lead name

### 4. Lead → Task Update (2 min)
- In Google Sheet, change lead status: "NEW" → "CONTACTED"
- Run: `.\run.ps1 sync` again
- Show in ClickUp: task status changed to "In Progress"

### 5. Task → Lead Update (2 min)
- In ClickUp, mark the task as "Done"
- Run: `.\run.ps1 sync` again
- Show in Google Sheet: lead status changed to "QUALIFIED"

### 6. Idempotency Test (1 min)
- Run: `.\run.ps1 sync` again (without changes)
- Show no duplicate tasks created
- Confirm sync completes without errors

## Recording Tools

**Option A: Windows Built-in (Recommended)**
- Press `Win + G` to open Game Bar
- Click "Start recording"
- Record your screen
- Press `Win + G` → "Stop recording"
- Video saved to `Videos\Captures\`

**Option B: OBS Studio (Free)**
- Download: https://obsproject.com/
- Set up scene (monitor capture)
- Start recording
- Stop when done
- Easily share video

**Option C: Camtasia / ScreenFlow (Paid)**
- Professional option
- Export as MP4

## Uploading to Google Drive

1. Go to https://drive.google.com
2. Click "New" → "File upload"
3. Select your video file
4. Wait for upload to complete
5. Right-click video → "Share"
6. Change sharing: "Anyone with the link can view"
7. Copy the link
8. Paste in README.md under "Video Demo" section

## Video Checklist

- [ ] Clear audio (use microphone)
- [ ] Good lighting (screen visible)
- [ ] Slow down typing (so viewers can follow)
- [ ] Show all 4 scenarios (create, lead→task update, task→lead update, idempotency)
- [ ] Less than 10 minutes
- [ ] Share link is public
- [ ] README updated with link

## Example README Update

```markdown
## Video Demo

Watch the complete demo: [2-way Sync Demo Video](https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing)

The video shows:
- Setup and configuration
- Creating a lead and syncing to ClickUp
- Updating lead status and task status
- Verifying idempotency
```

