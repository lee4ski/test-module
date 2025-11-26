# Test Suite Documentation

This directory contains comprehensive automated tests for the Data Comparison Tool.

## Test Structure

- `conftest.py` - Pytest fixtures and configuration
- `test_comparison_service.py` - Unit tests for the comparison service
- `test_api_endpoints.py` - API endpoint tests
- `test_ui_functionality.py` - UI/browser tests (button functionality, page interactions)
- `test_integration.py` - End-to-end integration tests

## Running Tests

### Prerequisites

1. Install dependencies:
```bash
make install-test-deps
# or
pip install -r requirements.txt
playwright install chromium
```

2. Start the server (for UI and integration tests):
```bash
python main.py
# or in another terminal
make run
```

### Run All Tests

```bash
# Using pytest directly
pytest tests/ -v

# Using Makefile
make test-all
```

### Run Specific Test Categories

```bash
# Unit tests only
make test-unit
# or
pytest tests/test_comparison_service.py -v -m unit

# API tests only
make test-api
# or
pytest tests/test_api_endpoints.py -v -m api

# UI tests only (requires server running)
make test-ui
# or
pytest tests/test_ui_functionality.py -v -m ui

# Integration tests only
make test-integration
# or
pytest tests/test_integration.py -v -m integration
```

### Run Tests with Coverage

```bash
make coverage
# or
pytest tests/ --cov=app --cov-report=html --cov-report=term
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Test individual functions and methods
- No external dependencies
- Fast execution
- Tests: `test_comparison_service.py`

### API Tests (`@pytest.mark.api`)
- Test HTTP endpoints
- Use FastAPI TestClient
- No browser required
- Tests: `test_api_endpoints.py`

### UI Tests (`@pytest.mark.ui`, `@pytest.mark.slow`)
- Test browser interactions
- Use Playwright for browser automation
- Test button clicks, form submissions, page navigation
- **Requires server to be running**
- Tests: `test_ui_functionality.py`

### Integration Tests (`@pytest.mark.integration`)
- Test complete workflows
- End-to-end scenarios
- Tests: `test_integration.py`

## What Gets Tested

### Button Functionality
- ✅ Choose File buttons exist and are visible
- ✅ Choose File buttons are clickable
- ✅ Compare Files button exists and works
- ✅ File input elements are properly configured
- ✅ Button cursor styles

### API Endpoints
- ✅ Root endpoint
- ✅ Upload page endpoint
- ✅ Results page endpoint
- ✅ Compare API endpoint
- ✅ Error handling for invalid files
- ✅ Response structure validation

### Service Logic
- ✅ File parsing (Excel and CSV)
- ✅ Value comparison
- ✅ Confidence calculation
- ✅ Normalization functions
- ✅ Error handling

### Integration
- ✅ Complete workflow with Excel files
- ✅ Complete workflow with CSV files
- ✅ Workflow with mismatches
- ✅ Confidence values in responses

## Pre-Deployment Checklist

Before deploying, ensure all tests pass:

```bash
# 1. Run all tests
make test-all

# 2. Check coverage
make coverage

# 3. Verify UI tests (with server running)
make test-ui
```

## Continuous Integration

Tests are configured to run automatically on:
- Push to main/develop branches
- Pull requests

See `.github/workflows/test.yml` for CI configuration.

## Troubleshooting

### UI Tests Failing
- Ensure the server is running on `http://localhost:8000`
- Check that Playwright browsers are installed: `playwright install chromium`
- Verify no firewall is blocking localhost connections

### Import Errors
- Ensure you're in the project root directory
- Verify all dependencies are installed: `pip install -r requirements.txt`

### File Parsing Errors
- Ensure `openpyxl` is installed for Excel support
- Check that test files are properly formatted



