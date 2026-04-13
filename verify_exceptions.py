"""
Manual verification script for RFC 9457 exceptions
"""
import sys
sys.path.insert(0, r'C:\Users\anchi\OneDrive\Escritorio\Facultad\4to\Ingenieria de software\NotebookUM')

from app.utils.exceptions import ProblemDetailException, InvalidPDFException

print("=== Testing ProblemDetailException ===")
exc1 = ProblemDetailException(
    type_uri="https://notebookum.com/problems/test",
    title="Test Problem",
    status=400,
    detail="Test detail message",
    instance="/api/test"
)
print(f"✓ Created ProblemDetailException")
print(f"  to_dict(): {exc1.to_dict()}")

print("\n=== Testing InvalidPDFException ===")
exc2 = InvalidPDFException(
    "The file does not have a valid PDF signature",
    instance="/api/pdf/extract"
)
print(f"✓ Created InvalidPDFException")
print(f"  type_uri: {exc2.type_uri}")
print(f"  title: {exc2.title}")
print(f"  status: {exc2.status}")
print(f"  detail: {exc2.detail}")
print(f"  to_dict(): {exc2.to_dict()}")

print("\n✅ All manual verifications passed!")
