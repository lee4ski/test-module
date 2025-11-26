# Quick Deploy to Vercel

## Option 1: Deploy via Vercel Dashboard (Easiest)

1. **Push to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push
   ```

2. **Go to Vercel**:
   - Visit https://vercel.com
   - Sign up/Login (free account works)
   - Click "Add New Project"
   - Import your GitHub repository

3. **Configure**:
   - Framework: **Other**
   - Root Directory: `Test module` (if repo is in subdirectory)
   - Build Command: Leave empty
   - Output Directory: Leave empty

4. **Add Environment Variable** (optional, for LLM):
   - Click "Environment Variables"
   - Add: `OPENAI_API_KEY` = `your-api-key-here`
   - See [LLM_SETUP.md](LLM_SETUP.md) for how to get your API key

5. **Deploy**:
   - Click "Deploy"
   - Wait ~2-3 minutes
   - Your app will be live! 🎉

## Option 2: Deploy via CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd "/Users/lee.sangmin/Repo/Test module"
vercel

# Add environment variable (if using LLM)
vercel env add OPENAI_API_KEY
# Paste your API key when prompted (see LLM_SETUP.md for how to get it)

# Deploy to production
vercel --prod
```

## Your App URL

After deployment, you'll get a URL like:
- `https://test-module-xyz.vercel.app`
- Or your custom domain if configured

## Access Your App

- Main page: `https://your-app.vercel.app/`
- Comparison tool: `https://your-app.vercel.app/comparison/`

## Notes

- **Free tier**: 100GB bandwidth/month, perfect for testing
- **Cold starts**: First request may be slow (~2-3 seconds), then fast
- **File size**: Large Excel files work, but be aware of 10-second timeout on free tier
- **LLM**: Works without API key (uses rule-based matching), or add key for enhanced matching

