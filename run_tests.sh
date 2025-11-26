#!/bin/bash

# Test runner script for Data Comparison Tool
# This script runs all tests and provides a summary

set -e

echo "🧪 Data Comparison Tool - Test Suite"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if server is running
check_server() {
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Server is running"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} Server is not running. UI tests will be skipped."
        echo "  Start server with: python main.py"
        return 1
    fi
}

# Run tests
run_tests() {
    local test_type=$1
    local test_name=$2
    
    echo ""
    echo "Running $test_name..."
    echo "----------------------------------------"
    
    if pytest tests/$test_type -v -m "$3" 2>&1; then
        echo -e "${GREEN}✓${NC} $test_name passed"
        return 0
    else
        echo -e "${RED}✗${NC} $test_name failed"
        return 1
    fi
}

# Check dependencies
echo "Checking dependencies..."
if ! python -c "import pytest" 2>/dev/null; then
    echo -e "${RED}✗${NC} pytest not installed"
    echo "  Install with: pip install -r requirements.txt"
    exit 1
fi

if ! python -c "import playwright" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC} playwright not installed (UI tests will be skipped)"
    echo "  Install with: pip install playwright && playwright install chromium"
fi

SERVER_RUNNING=0
check_server || SERVER_RUNNING=1

# Track results
UNIT_PASSED=0
API_PASSED=0
UI_PASSED=0
INTEGRATION_PASSED=0

# Run unit tests
if run_tests "test_comparison_service.py" "Unit Tests" "unit"; then
    UNIT_PASSED=1
fi

# Run API tests
if run_tests "test_api_endpoints.py" "API Tests" "api"; then
    API_PASSED=1
fi

# Run integration tests
if run_tests "test_integration.py" "Integration Tests" "integration"; then
    INTEGRATION_PASSED=1
fi

# Run UI tests only if server is running
if [ $SERVER_RUNNING -eq 0 ]; then
    if run_tests "test_ui_functionality.py" "UI Tests" "ui"; then
        UI_PASSED=1
    fi
else
    echo ""
    echo -e "${YELLOW}⚠${NC} UI tests skipped (server not running)"
fi

# Summary
echo ""
echo "======================================"
echo "Test Summary"
echo "======================================"
echo -e "Unit Tests:        $([ $UNIT_PASSED -eq 1 ] && echo -e "${GREEN}✓ PASSED${NC}" || echo -e "${RED}✗ FAILED${NC}")"
echo -e "API Tests:          $([ $API_PASSED -eq 1 ] && echo -e "${GREEN}✓ PASSED${NC}" || echo -e "${RED}✗ FAILED${NC}")"
echo -e "Integration Tests: $([ $INTEGRATION_PASSED -eq 1 ] && echo -e "${GREEN}✓ PASSED${NC}" || echo -e "${RED}✗ FAILED${NC}")"
echo -e "UI Tests:           $([ $SERVER_RUNNING -eq 0 ] && ([ $UI_PASSED -eq 1 ] && echo -e "${GREEN}✓ PASSED${NC}" || echo -e "${RED}✗ FAILED${NC}") || echo -e "${YELLOW}⚠ SKIPPED${NC}")"
echo ""

# Exit with error if any test failed
if [ $UNIT_PASSED -eq 0 ] || [ $API_PASSED -eq 0 ] || [ $INTEGRATION_PASSED -eq 0 ]; then
    echo -e "${RED}Some tests failed. Please fix issues before deployment.${NC}"
    exit 1
fi

if [ $SERVER_RUNNING -eq 0 ] && [ $UI_PASSED -eq 0 ]; then
    echo -e "${RED}UI tests failed. Please fix issues before deployment.${NC}"
    exit 1
fi

echo -e "${GREEN}All tests passed! Ready for deployment.${NC}"
exit 0



