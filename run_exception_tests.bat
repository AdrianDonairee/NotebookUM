@echo off
echo Running RFC 9457 Exception Tests...
echo.

python tests\test_rfc9457_exceptions.py
if %errorlevel% neq 0 (
    echo FAILED: test_rfc9457_exceptions.py
    exit /b 1
)

echo.
echo Tests completed!
