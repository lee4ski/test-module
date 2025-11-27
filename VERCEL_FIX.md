# Fixing Vercel Deployment

## Issue
Deployments are not showing up in Vercel dashboard even though commits are being pushed.

## Solution Steps

### 1. Verify Repository Connection
1. Go to: https://vercel.com/lee4skis-projects/test-module/settings/git
2. Verify that `lee4ski/test-module` is connected
3. If not connected, click "Connect Git Repository" and select your repo

### 2. Check GitHub Webhook
1. Go to: https://github.com/lee4ski/test-module/settings/hooks
2. Look for a Vercel webhook
3. If missing or failed, you may need to reconnect the repository in Vercel

### 3. Manually Trigger Deployment
If automatic deployments aren't working:

**Option A: Via Vercel Dashboard**
1. Go to: https://vercel.com/lee4skis-projects/test-module
2. Click the "..." menu (three dots) next to the project
3. Select "Redeploy" or look for a "Deploy" button
4. Select the latest commit and deploy

**Option B: Create Deploy Hook**
1. Go to: https://vercel.com/lee4skis-projects/test-module/settings/git
2. Scroll to "Deploy Hooks"
3. Click "Create Hook"
4. Name it (e.g., "Manual Deploy")
5. Copy the hook URL
6. Use it to trigger deployments:
   ```bash
   curl -X POST https://api.vercel.com/v1/integrations/deploy/your-hook-url
   ```

**Option C: Disconnect and Reconnect**
1. Go to: https://vercel.com/lee4skis-projects/test-module/settings/git
2. Click "Disconnect" next to the repository
3. Click "Connect Git Repository" again
4. Select `lee4ski/test-module`
5. This will trigger a new deployment

### 4. Verify Configuration
The `vercel.json` should have:
- `src: "api/index.py"` in builds
- `dest: "api/index.py"` in routes (no leading slash)
- `maxDuration: 30` for the function

### 5. Check Build Logs
1. Go to: https://vercel.com/lee4skis-projects/test-module/deployments
2. Click on any deployment (if visible)
3. Check the build logs for errors

### 6. Environment Variables
Make sure environment variables are set:
1. Go to: https://vercel.com/lee4skis-projects/test-module/settings/environment-variables
2. Add `OPENAI_API_KEY` if using LLM (optional)

## Current Configuration

- **Entry Point**: `api/index.py`
- **Handler**: `handler` (exported from Mangum)
- **Routes**: All routes (`/(.*)`) go to `api/index.py`
- **Max Duration**: 30 seconds

## Testing the Deployment

After deployment, test:
- Root: `https://test-module.vercel.app/`
- Comparison page: `https://test-module.vercel.app/comparison/`
- API: `https://test-module.vercel.app/api/comparison/compare`

## If Still Not Working

1. Check Vercel status: https://vercel-status.com
2. Try creating a new Vercel project and importing the repository fresh
3. Check if there are any build errors in the logs
4. Verify that `requirements.txt` includes all dependencies, especially `mangum`

