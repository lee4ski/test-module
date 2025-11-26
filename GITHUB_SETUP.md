# GitHub Setup for Vercel Deployment

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `test-module` (or any name you prefer)
3. Description: "Data Comparison Tool - Excel file comparison with LLM column matching"
4. Choose: **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

## Step 2: Push Your Code

After creating the repository, GitHub will show you commands. Use these:

```bash
cd "/Users/lee.sangmin/Repo/Test module"

# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/test-module.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Vercel

After pushing to GitHub:

1. Go to https://vercel.com
2. Sign up/Login (use GitHub to sign in - easiest!)
3. Click **"Add New..."** → **"Project"**
4. Find and select your `test-module` repository
5. Click **"Import"**

## Step 4: Configure Vercel Project

1. **Framework Preset**: Select **"Other"**
2. **Root Directory**: 
   - If your repo only contains the Test module: Leave empty
   - If your repo has multiple folders: Enter `Test module`
3. **Build Command**: Leave empty
4. **Output Directory**: Leave empty
5. **Install Command**: `pip install -r requirements.txt`

## Step 5: Add Environment Variables

1. Click **"Environment Variables"** section
2. Click **"Add"**
3. Name: `OPENAI_API_KEY`
4. Value: `YOUR_OPENAI_API_KEY_HERE`
5. Select environments: **Production**, **Preview**, **Development**
6. Click **"Add"**

## Step 6: Deploy!

1. Click **"Deploy"** button
2. Wait 2-3 minutes for build to complete
3. Your app will be live! 🎉

## Your Live URL

After deployment, Vercel will show you:
- **Production URL**: `https://test-module.vercel.app` (or similar)
- **Preview URLs**: For each commit/branch

## Access Your App

- Main page: `https://your-app.vercel.app/`
- Comparison tool: `https://your-app.vercel.app/comparison/`

## Troubleshooting

### Build Fails
- Check that `requirements.txt` is in the root
- Verify Python version (Vercel uses 3.9 by default)
- Check build logs in Vercel dashboard

### Import Errors
- Make sure `api/index.py` exists
- Verify all files are committed to git

### Environment Variables Not Working
- Make sure you selected all environments (Production, Preview, Development)
- Redeploy after adding variables

