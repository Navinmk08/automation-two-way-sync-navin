# GitHub Setup Guide

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `automation-two-way-sync`
3. Description: `Two-way sync between Google Sheets and ClickUp`
4. Choose **Private** (optional, can be public)
5. Click "Create repository"

## Step 2: Initialize Local Git Repository

From the project root:

```powershell
cd C:\Users\navin\Desktop\automation-two-way-sync

# Initialize git
git init

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/automation-two-way-sync.git

# Create main branch
git branch -M main
```

## Step 3: Add All Files

```powershell
# Stage all files
git add .

# Check status
git status

# Commit
git commit -m "Initial commit: two-way sync implementation"
```

## Step 4: Push to GitHub

```powershell
# Push to GitHub
git push -u origin main

# Verify
git log --oneline
```

## Step 5: Share Repository Access

1. Go to your GitHub repo: `https://github.com/YOUR_USERNAME/automation-two-way-sync`
2. Click "Settings" → "Collaborators"
3. Click "Add people"
4. Add:
   - `deeplogicaitech`
   - `csvinay`
5. Grant them "Maintainer" or "Write" access

## Step 6: Configure GitHub Actions

The CI/CD workflow is already in `.github/workflows/tests.yml`

It will:
- Run on every push to `main` or `develop`
- Run daily at 2 AM UTC
- Execute all tests with pytest
- Check Python syntax

To verify it's working:
1. Push a change
2. Go to your repo → "Actions"
3. You should see a test run

## Troubleshooting

- **"fatal: not a git repository"**: Run `git init` first
- **"fatal: origin already exists"**: Run `git remote rm origin` then add again
- **"Permission denied"**: Make sure you're logged into GitHub via git credentials
- **"Authentication failed"**: Use a Personal Access Token (PAT) instead of password

