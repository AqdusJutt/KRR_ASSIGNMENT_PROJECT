# GitHub Setup Guide

## Step 1: Initialize Git Repository

```powershell
# Navigate to project
cd E:\KRR_ASSIGNMENT_PROJECT

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Multi-Agent Chat System - Complete implementation"
```

## Step 2: Create GitHub Repository

1. **Go to GitHub:** https://github.com
2. **Click:** "New repository" (or the "+" icon)
3. **Repository name:** `KRR_ASSIGNMENT_PROJECT` (or your preferred name)
4. **Description:** "Multi-Agent Chat System for Knowledge Representation and Reasoning"
5. **Visibility:** Public (required for assignment)
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. **Click:** "Create repository"

## Step 3: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```powershell
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/KRR_ASSIGNMENT_PROJECT.git

# Or if you prefer SSH:
# git remote add origin git@github.com:YOUR_USERNAME/KRR_ASSIGNMENT_PROJECT.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Verify

1. Go to your GitHub repository page
2. You should see all your files there
3. Check that `.env` is NOT uploaded (it should be in `.gitignore`)

## Quick Commands Reference

```powershell
# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your commit message here"

# Push to GitHub
git push

# Pull latest changes
git pull
```

## Important Notes

- ✅ **Make sure `.env` is in `.gitignore`** (it contains your API key!)
- ✅ **Keep repository public** (assignment requirement)
- ✅ **Both team members should commit** (shows collaboration)

## Example Workflow for Future Updates

```powershell
# 1. Check what changed
git status

# 2. Add changes
git add .

# 3. Commit with descriptive message
git commit -m "Added privacy knowledge base and fixed memory retrieval"

# 4. Push to GitHub
git push
```

## Troubleshooting

### "Repository not found" error?
- Check your GitHub username is correct
- Make sure repository exists on GitHub
- Verify you have access (if it's a team repository)

### "Permission denied" error?
- You may need to authenticate
- Use GitHub Personal Access Token instead of password
- Or set up SSH keys

### Want to update existing repository?
```powershell
git add .
git commit -m "Updated: [describe your changes]"
git push
```

