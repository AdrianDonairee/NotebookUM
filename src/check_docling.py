"""
Quick test to understand docling API with bytes
"""
import sys
sys.path.insert(0, r'C:\Users\anchi\OneDrive\Escritorio\Facultad\4to\Ingenieria de software\NotebookUM')

# Check docling API
try:
    from docling.document_converter import DocumentConverter
    import io
    print("✓ docling imported successfully")
    print(f"DocumentConverter available: {DocumentConverter}")
    print(f"DocumentConverter methods: {[m for m in dir(DocumentConverter) if not m.startswith('_')]}")
except Exception as e:
    print(f"Error importing docling: {e}")
