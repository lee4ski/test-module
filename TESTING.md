# Testing Guide

## Overview

This project includes comprehensive automated tests covering:
- ✅ Unit tests for service logic
- ✅ API endpoint tests
- ✅ UI/browser tests (button functionality, form interactions)
- ✅ Integration tests (end-to-end workflows)

## Quick Start

### 1. Install Dependencies

```bash
# Install all dependencies including test tools
make install-test-deps

# Or manually:
pip install -r requirements.txt
playwright install chromium
```

### 2. Run Tests

```bash
# Run all tests
make test-all

# Or use the test runner script
./run_tests.sh

# Or use pytest directly
pytest tests/ -v
```

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_comparison_service.py  # Unit tests
├── test_api_endpoints.py       # API tests
├── test_ui_functionality.py   # UI/browser tests
└── test_integration.py        # Integration tests
```

## Running Specific Tests

### Unit Tests Only
```bash
make test-unit
# Tests service logic, file parsing, confidence calculation
```

### API Tests Only
```bash
make test-api
# Tests HTTP endpoints, request/response handling
```

### UI Tests Only
```bash
# First, start the server
python main.py

# Then in another terminal
make test-ui
# Tests button clicks, form submissions, page navigation
```

### Integration Tests Only
```bash
make test-integration
# Tests complete workflows end-to-end
```

## What Gets Tested

### Button Functionality ✅
- Choose File buttons exist and are visible
- Choose File buttons are clickable
- Compare Files button works correctly
- File input elements are properly configured
- Navigation buttons function correctly

### API Endpoints ✅
- All endpoints return correct status codes
- Request validation works
- Error handling for invalid inputs
- Response structure is correct
- File upload and processing works

### Service Logic ✅
- File parsing (Excel and CSV)
- Value comparison logic
- Confidence calculation
- Value normalization
- Error handling

### Integration ✅
- Complete workflow with Excel files
- Complete workflow with CSV files
- Handling of mismatches
- Confidence values in responses

## Test Coverage

Generate coverage report:

```bash
make coverage
```

This will:
- Run all tests
- Generate HTML coverage report in `htmlcov/`
- Show terminal coverage summary

## Pre-Deployment Testing

Before deploying, run the complete test suite:

```bash
# 1. Ensure server is running (for UI tests)
python main.py &

# 2. Run all tests
./run_tests.sh

# 3. Check coverage
make coverage
```

The test runner script (`run_tests.sh`) will:
- Check if server is running
- Run all test categories
- Provide a summary of results
- Exit with error code if any test fails

## Continuous Integration

Tests automatically run on:
- Push to main/develop branches
- Pull requests

See `.github/workflows/test.yml` for CI configuration.

## Troubleshooting

### UI Tests Not Running
**Problem**: UI tests fail or are skipped

**Solution**:
1. Ensure server is running: `python main.py`
2. Check server is accessible: `curl http://localhost:8000/`
3. Install Playwright browsers: `playwright install chromium`

### Import Errors
**Problem**: `ModuleNotFoundError` when running tests

**Solution**:
1. Install dependencies: `pip install -r requirements.txt`
2. Ensure you're in the project root directory
3. Check Python path includes the project directory

### File Parsing Errors
**Problem**: Tests fail with file parsing errors

**Solution**:
1. Ensure `openpyxl` is installed: `pip install openpyxl`
2. Check test fixtures in `conftest.py` are correct

## Test Markers

Tests are organized with markers for easy filtering:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.api` - API tests
- `@pytest.mark.ui` - UI/browser tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow running tests

Run tests by marker:
```bash
pytest -m unit        # Only unit tests
pytest -m "not slow"  # Skip slow tests
pytest -m "api or unit"  # API or unit tests
```

## Writing New Tests

### Adding a Unit Test

```python
@pytest.mark.unit
def test_my_function():
    service = ComparisonService()
    result = service.my_function()
    assert result == expected_value
```

### Adding an API Test

```python
@pytest.mark.api
def test_my_endpoint(client):
    response = client.get("/my-endpoint")
    assert response.status_code == 200
```

### Adding a UI Test

```python
@pytest.mark.ui
def test_my_button(page):
    page.goto("http://localhost:8000/comparison/")
    button = page.locator("button:has-text('My Button')")
    button.click()
    # Assert expected behavior
```

## Best Practices

1. **Run tests before committing**: `make test-all`
2. **Keep tests fast**: Unit tests should be < 1 second each
3. **Test edge cases**: Empty files, invalid formats, etc.
4. **Use fixtures**: Reuse test data from `conftest.py`
5. **Clear test names**: Test names should describe what they test
6. **One assertion per concept**: Don't test multiple things in one test

## CI/CD Integration

The test suite is configured to run automatically in CI/CD pipelines. The GitHub Actions workflow (`.github/workflows/test.yml`) will:

1. Install dependencies
2. Start the server
3. Run all test categories
4. Generate coverage reports
5. Fail the build if any test fails

This ensures code quality before merging to main branches.



