# LLM Setup Guide for Column Matching

This guide explains how to set up OpenAI API keys for enhanced column matching that can handle different languages and naming conventions.

## Why Use LLM Matching?

LLM-based matching can:
- Match columns across languages (e.g., "Name" ↔ "名前")
- Understand semantic meaning (e.g., "Amount" ↔ "金額")
- Handle abbreviations and different naming conventions
- Work even when column names are completely different but represent the same data

## Option 1: OpenAI (Recommended for Testing)

### Step 1: Get Your API Key

1. Visit https://platform.openai.com/
2. Sign in or create an account
3. Go to API Keys: https://platform.openai.com/api-keys
4. Click **"Create new secret key"**
5. Give it a name (e.g., "Test Module Column Matching")
6. Click **"Create secret key"**
7. **Copy the key immediately** - you won't be able to see it again!

### Step 2: Set Environment Variable

**On macOS/Linux:**
```bash
export OPENAI_API_KEY="sk-..."
```

**On Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-...
```

**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-..."
```

**To make it permanent**, add to your `~/.bashrc`, `~/.zshrc`, or `.env` file:
```bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Verify Setup

```bash
cd "/Users/lee.sangmin/Repo/Test module"
python -c "from app.services.comparison import ComparisonService; s = ComparisonService(); print('LLM Available:', s.llm_client is not None)"
```

Should output: `LLM Available: True`

## Option 2: Azure OpenAI

If your organization uses Azure OpenAI:

### Step 1: Get Azure OpenAI Credentials

1. Go to https://portal.azure.com/
2. Search for "Azure OpenAI" in the top search bar
3. Select your Azure OpenAI resource
4. Go to **"Keys and Endpoint"** in the left menu
5. Copy:
   - **Key 1** or **Key 2** (either works)
   - **Endpoint** URL

### Step 2: Set Environment Variables

```bash
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_API_VERSION="2024-10-21"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o"  # Optional, defaults to gpt-4o
```

## Testing the Setup

1. Start the server:
```bash
python main.py
```

2. Upload an Excel file with columns in different languages or naming conventions

3. The system will automatically use LLM matching if the API key is configured

## Troubleshooting

### "LLM Available: False"

- Check that the environment variable is set: `echo $OPENAI_API_KEY`
- Make sure you've restarted your terminal/server after setting the variable
- Verify the API key is correct (starts with `sk-` for OpenAI)

### "Failed to initialize LLM client"

- Check your API key is valid
- For Azure: verify endpoint URL is correct
- Check your internet connection
- Verify you have credits/quota in your OpenAI account

### API Key Not Working

- Make sure there are no extra spaces or quotes in the key
- For Azure: ensure the deployment name matches your actual deployment
- Check if your API key has expired or been revoked

## Cost Considerations

- OpenAI charges per API call (very small cost per column matching operation)
- Typical cost: ~$0.0001-0.001 per comparison
- You can set usage limits in your OpenAI account settings
- The system falls back to rule-based matching if LLM fails, so costs are minimal

## Security Notes

⚠️ **Never commit API keys to git!**

- Use environment variables (as shown above)
- Add `.env` to `.gitignore` if using a `.env` file
- Use secret management tools in production

## Without API Key

The system works perfectly fine without an API key! It will use:
1. Rule-based matching (case-insensitive, fuzzy matching)
2. Position-based matching as fallback

LLM matching is an **enhancement**, not a requirement.

