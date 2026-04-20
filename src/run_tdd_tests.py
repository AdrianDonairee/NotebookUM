"""
Test runner script for TDD workflow
"""
import sys
import unittest

# Add the project root to the path
sys.path.insert(0, r'C:\Users\anchi\OneDrive\Escritorio\Facultad\4to\Ingenieria de software\NotebookUM')

# Import the test module
from tests import test_rfc9457_exceptions

# Create test suite
loader = unittest.TestLoader()
suite = loader.loadTestsFromModule(test_rfc9457_exceptions)

# Run tests with verbose output
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Exit with appropriate code
sys.exit(0 if result.wasSuccessful() else 1)
