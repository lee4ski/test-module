# Test Module - Data Comparison Tool

A FastAPI-based web application for comparing Excel files with intelligent column matching using LLM.

## Features

- 📊 Compare Excel files with two tabs: "正解データ" (Ground Truth) and "Robota結果" (Robota Results)
- 🤖 LLM-enhanced semantic column matching (supports OpenAI and Azure OpenAI)
- 📈 Detailed cell-level statistics (total cells, matched, mismatched, accuracy)
- 🎯 Flexible column matching (order-independent, case-insensitive, fuzzy matching)
- 🌐 Web-based interface with beautiful UI

## Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Access the app**:
   - Main page: http://localhost:8000
   - Comparison tool: http://localhost:8000/comparison/

### Deployment

#### Railway (Recommended)

1. **Sign up at Railway**: https://railway.app
2. **Create a new project** and connect your GitHub repository
3. **Set environment variables** (if using LLM):
   - `OPENAI_API_KEY` (for OpenAI)
   - Or Azure OpenAI variables (see [LLM_SETUP.md](LLM_SETUP.md))
4. **Deploy**: Railway will automatically deploy on push

See [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md) for detailed instructions.

## Project Structure

```
Test module/
├── app/
│   ├── routers/          # API routes
│   ├── schemas/          # Pydantic models
│   └── services/         # Business logic
├── templates/            # HTML templates
├── main.py               # FastAPI application entry point
├── requirements.txt      # Python dependencies
└── railway.json          # Railway configuration
```

## Configuration

### LLM Setup (Optional)

The application works without LLM (uses rule-based matching), but LLM enhances column matching for:
- Cross-language matching
- Semantic similarity
- Complex column name variations

See [LLM_SETUP.md](LLM_SETUP.md) for setup instructions.

## API Endpoints

- `GET /` - Root endpoint
- `GET /comparison/` - Upload page
- `POST /api/comparison/compare` - Compare files
- `GET /comparison/results/{result_id}` - View results

## Testing

Run tests with:
```bash
pytest
```

## License

MIT
