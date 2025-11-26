.PHONY: test test-unit test-api test-ui test-integration test-all install install-test-deps run coverage

# Install dependencies
install:
	pip install -r requirements.txt

# Install test dependencies (including playwright browsers)
install-test-deps: install
	playwright install chromium

# Run all tests
test-all:
	pytest tests/ -v

# Run unit tests only
test-unit:
	pytest tests/test_comparison_service.py -v -m unit

# Run API tests only
test-api:
	pytest tests/test_api_endpoints.py -v -m api

# Run UI tests only
test-ui:
	pytest tests/test_ui_functionality.py -v -m ui

# Run integration tests only
test-integration:
	pytest tests/test_integration.py -v -m integration

# Run tests with coverage
coverage:
	pytest tests/ --cov=app --cov-report=html --cov-report=term

# Run the application
run:
	python main.py

# Quick test (unit + api, no UI)
test:
	pytest tests/test_comparison_service.py tests/test_api_endpoints.py -v



