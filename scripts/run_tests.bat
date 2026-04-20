@echo off
echo Running PDF File Validator Tests...
echo.

echo ========================================
echo Test 1: File Validator Service Tests
echo ========================================
python tests\test_file_validator.py
if %errorlevel% neq 0 (
    echo FAILED: test_file_validator.py
    exit /b 1
)

echo.
echo ========================================
echo Test 2: File Validation Endpoint Tests
echo ========================================
python tests\test_file_endpoint.py
if %errorlevel% neq 0 (
    echo FAILED: test_file_endpoint.py
    exit /b 1
)

echo.
echo ========================================
echo All Tests Passed! ✓
echo ========================================
