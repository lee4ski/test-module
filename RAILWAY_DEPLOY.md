# Deploying to Railway

This guide explains how to deploy the Test Module to Railway.

## Prerequisites

1. **Railway Account**: Sign up at https://railway.app (free account works)
2. **GitHub Account**: Your code should be in a GitHub repository

## Deployment Steps

### Method 1: Deploy via Railway Dashboard (Recommended)

1. **Go to Railway**:
   - Visit https://railway.app
   - Sign up/Login (free account works)
   - Click "New Project"

2. **Connect GitHub Repository**:
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub account
   - Select your repository: `lee4ski/test-module`
   - Railway will automatically detect it's a Python project

3. **Configure Environment Variables** (if using LLM):
   - Go to your project → Variables
   - Add:
     - `OPENAI_API_KEY` = `your-api-key-here`
     - Or for Azure OpenAI:
       - `AZURE_OPENAI_API_KEY`
       - `AZURE_OPENAI_ENDPOINT`
       - `AZURE_OPENAI_API_VERSION`
       - `AZURE_OPENAI_DEPLOYMENT`

4. **Deploy**:
   - Railway will automatically start building
   - Wait for build to complete (~2-3 minutes)
   - Your app will be live at `https://your-project.railway.app`

5. **Get Your URL**:
   - Go to Settings → Generate Domain
   - Or use the automatically generated domain

### Method 2: Deploy via Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login**:
   ```bash
   railway login
   ```

3. **Initialize Project**:
   ```bash
   cd "/Users/lee.sangmin/Repo/Test module"
   railway init
   ```

4. **Deploy**:
   ```bash
   railway up
   ```

5. **Set Environment Variables** (if using LLM):
   ```bash
   railway variables set OPENAI_API_KEY=your-api-key-here
   ```

## Project Structure

Railway will automatically detect:
- `requirements.txt` - Python dependencies
- `Procfile` or `railway.json` - Start command
- `main.py` - Entry point

## Important Notes

### Port Configuration
- Railway sets the `PORT` environment variable automatically
- The app listens on `0.0.0.0:$PORT` as configured

### Environment Variables
- **Required**: None (works without LLM)
- **Optional**: `OPENAI_API_KEY` for LLM-enhanced column matching

### File Size Limits
- Railway has generous limits for file uploads
- Large Excel files should work fine

### Cold Starts
- First request after inactivity may be slow (~2-3 seconds)
- Subsequent requests are fast

## Troubleshooting

### Build Fails
- Check that `requirements.txt` is correct
- Ensure Python version is compatible (3.11+)
- Check build logs in Railway dashboard

### Import Errors
- Make sure all dependencies are in `requirements.txt`
- Check that file paths are correct

### Port Issues
- Make sure the app listens on `0.0.0.0` and uses `$PORT`
- Check Railway logs for port binding errors

### Environment Variables Not Working
- Make sure variables are set in Railway dashboard
- Redeploy after adding environment variables
- Check variable names match exactly (case-sensitive)

## Access Your App

After deployment, you'll get a URL like:
- `https://test-module-production.up.railway.app`
- Or your custom domain if configured

## Monitoring

- View logs in Railway Dashboard → Deployments → Logs
- Monitor resource usage in the dashboard
- Set up alerts for failures

## Cost

- **Free Tier**: 
  - $5 credit/month
  - 500 hours of usage
  - Perfect for testing and small projects

## Migration from Vercel

If you were previously using Vercel:
1. Railway is better suited for Python/FastAPI apps
2. No need for `api/index.py` or `mangum` wrapper
3. Direct deployment of FastAPI app
4. Better support for file uploads and long-running requests

