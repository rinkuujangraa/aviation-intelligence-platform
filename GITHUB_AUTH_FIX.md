# GitHub Authentication Fix

## Problem
Git is configured with a different account than your repository owner.

## Solution: Use Personal Access Token

### Step 1: Create Personal Access Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it: `Aviation Intelligence Deploy`
4. Select scopes: ✅ `repo` (all checkboxes under it)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)

### Step 2: Push with Token
Run these commands in Git Bash or PowerShell:

```bash
# Set remote with token authentication
git remote add origin https://YOUR_TOKEN@github.com/rinkuujangraa/indian-avitation-intelligence.git

# Push to GitHub
git push -u origin main
```

Replace `YOUR_TOKEN` with the token you copied.

### Alternative: SSH Method

If you prefer SSH:

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your.email@gmail.com"

# Copy the public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: https://github.com/settings/ssh/new

# Set remote with SSH
git remote add origin git@github.com:rinkuujangraa/indian-avitation-intelligence.git

# Push
git push -u origin main
```

## Quick Commands (After Token/SSH Setup)

```bash
# Add remote (choose ONE):
git remote add origin https://YOUR_TOKEN@github.com/rinkuujangraa/indian-avitation-intelligence.git
# OR
git remote add origin git@github.com:rinkuujangraa/indian-avitation-intelligence.git

# Push
git push -u origin main
```

## Verify Success
After pushing, visit: https://github.com/rinkuujangraa/indian-avitation-intelligence

You should see all your files!
