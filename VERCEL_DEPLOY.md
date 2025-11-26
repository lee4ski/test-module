# Deploying to Vercel

This guide explains how to deploy the Test Module to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at https://vercel.com (free account works)
2. **Vercel CLI** (optional, for command-line deployment):
   ```bash
   npm install -g vercel
   ```

## Deployment Methods

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Go to Vercel Dashboard**:
   - Visit https://vercel.com/dashboard
   - Click "Add New..." → "Project"
   - Import your GitHub repository

3. **Configure Project**:
   - **Framework Preset**: Other
   - **Root Directory**: `Test module` (if repo is in subdirectory)
   - **Build Command**: Leave empty (Vercel will auto-detect)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

4. **Set Environment Variables**:
   - Go to Project Settings → Environment Variables
   - Add if using LLM:
     - `OPENAI_API_KEY` = `sk-proj-...` (your API key)
     - Or for Azure OpenAI:
       - `AZURE_OPENAI_API_KEY`
       - `AZURE_OPENAI_ENDPOINT`
       - `AZURE_OPENAI_API_VERSION`

5. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live at `https://your-project.vercel.app`

### Method 2: Deploy via CLI

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   cd "/Users/lee.sangmin/Repo/Test module"
   vercel
   ```

4. **Set Environment Variables** (if using LLM):
   ```bash
   vercel env add OPENAI_API_KEY
   # Paste your API key when prompted
   ```

5. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

## Project Structure for Vercel

```
Test module/
├── api/
│   └── index.py          # Vercel serverless function entry point
├── app/                   # Your application code
├── templates/             # HTML templates
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
└── main.py                # FastAPI app
```

## Important Notes

### File Size Limits
- Vercel has a 50MB limit for serverless functions
- Large dependencies (like pandas, openpyxl) should work, but be aware of limits
- If you hit limits, consider using Vercel Pro plan or alternative hosting

### Environment Variables
- **Required**: None (works without LLM)
- **Optional**: `OPENAI_API_KEY` for LLM-enhanced column matching

### Cold Starts
- First request after inactivity may be slow (cold start)
- Subsequent requests are fast
- Consider Vercel Pro for better performance

### Function Timeout
- Free tier: 10 seconds
- Pro tier: 60 seconds
- Large Excel files may take longer - monitor timeout limits

## Troubleshooting

### Build Fails
- Check that `requirements.txt` is correct
- Ensure Python version is compatible (Vercel uses Python 3.9 by default)
- Check build logs in Vercel dashboard

### Import Errors
- Make sure `api/index.py` correctly imports from parent directory
- Check that all dependencies are in `requirements.txt`

### Timeout Issues
- Large files may exceed function timeout
- Consider adding file size validation
- Or upgrade to Vercel Pro for longer timeouts

### Environment Variables Not Working
- Make sure variables are set in Vercel dashboard
- Redeploy after adding environment variables
- Check variable names match exactly (case-sensitive)

## Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

## Monitoring

- View logs in Vercel Dashboard → Project → Logs
- Monitor function execution time and errors
- Set up alerts for failures

## Cost

- **Free Tier**: 
  - 100GB bandwidth/month
  - 100 hours execution time/month
  - Perfect for testing and small projects

- **Pro Tier** ($20/month):
  - Unlimited bandwidth
  - Better performance
  - Longer timeouts (60s)

