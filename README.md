# Test Module - Data Comparison Tool

A web-based tool for comparing ground truth data (正解データ) with extracted results (読取結果) and generating confidence levels for verification.

## Features

- 📊 Upload and compare Excel (.xlsx, .xls) or CSV files
- ✅ Visual match/mismatch indicators for each cell
- 📈 Confidence level calculation (percentage) for mismatched cells
- 🎨 Modern, user-friendly web interface
- 📋 Table view matching spreadsheet structure

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Deployment to Vercel

This app is ready to deploy to Vercel! See [DEPLOY.md](DEPLOY.md) for quick deployment instructions.

**Quick deploy:**
1. Push code to GitHub
2. Import to Vercel (https://vercel.com)
3. Add environment variable `OPENAI_API_KEY` (optional, for LLM matching)
4. Deploy!

Your app will be live at `https://your-project.vercel.app`

### Optional: LLM-Enhanced Column Matching

For better column matching (especially across languages or different naming conventions), you can configure OpenAI.

**Quick Setup:**
1. Get your API key from https://platform.openai.com/api-keys
2. Set it: `export OPENAI_API_KEY="sk-..."`
3. Restart the server

**For detailed instructions**, see [LLM_SETUP.md](LLM_SETUP.md)

**For Azure OpenAI:**
```bash
export AZURE_OPENAI_API_KEY="your-api-key-here"
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_OPENAI_API_VERSION="2024-10-21"
```

If no API key is configured, the system will use rule-based matching (case-insensitive, fuzzy matching).

## Usage

1. Start the server:
```bash
python main.py
```

2. Open your browser and navigate to:
```
http://localhost:8000/comparison/
```

3. Upload two files:
   - **正解データ (Ground Truth Data)**: The correct/reference data
   - **読取結果 (Extracted Results)**: The extracted/read results to compare

4. Click "Compare Files" to see the results

## How It Works

1. **File Parsing**: Supports both Excel and CSV files (with UTF-8 and Shift-JIS encoding)
2. **Comparison**: Compares each cell value between the two files
3. **Confidence Calculation**: Uses sequence matching algorithm to calculate similarity percentage for mismatched cells
4. **Visualization**: 
   - Green cells indicate matches
   - Red cells indicate mismatches with confidence percentage badges
   - Color-coded confidence levels (high/medium/low)

## API Endpoints

- `GET /comparison/` - Upload page
- `GET /comparison/results` - Results page
- `POST /comparison/api/compare` - API endpoint for file comparison (returns JSON)

## Project Structure

```
Test module/
├── main.py                 # FastAPI application entry point
├── app/
│   ├── routers/
│   │   └── comparison.py   # API routes
│   ├── services/
│   │   └── comparison.py   # Comparison logic
│   └── schemas/
│       └── comparison.py # Pydantic models
├── templates/
│   ├── index.html         # Upload page
│   └── results.html       # Results display page
└── requirements.txt       # Python dependencies
```

## Testing

The project includes a comprehensive automated test suite to ensure all functionalities work correctly before deployment.

### Quick Start

```bash
# Install test dependencies
make install-test-deps

# Run all tests
make test-all

# Or use the test runner script
./run_tests.sh
```

### Test Categories

- **Unit Tests**: Test individual service functions
- **API Tests**: Test HTTP endpoints
- **UI Tests**: Test browser interactions and button functionality
- **Integration Tests**: Test complete workflows

See [tests/README.md](tests/README.md) for detailed testing documentation.

### Pre-Deployment Checklist

Before deploying, ensure all tests pass:

```bash
# Run all tests
make test-all

# Check test coverage
make coverage

# Verify UI tests (requires server running)
make test-ui
```

## Notes

- The tool assumes both files have the same column structure
- Missing values are treated as empty strings
- Numbers are normalized for comparison (trailing zeros removed)
- Confidence levels are calculated using sequence matching (0-100%)

