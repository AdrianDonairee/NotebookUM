"""
File signature validation service.
Validates files based on their byte signatures (magic numbers).
"""

# PDF file signature according to https://en.wikipedia.org/wiki/List_of_file_signatures
PDF_SIGNATURE = b'%PDF'  # Hex: 25 50 44 46


def validate_pdf_signature(file_bytes: bytes) -> bool:
    """
    Validates if the given bytes start with a valid PDF signature.
    
    According to the file signatures standard, PDF files start with
    the bytes 25 50 44 46 (ASCII: %PDF) at offset 0.
    
    Args:
        file_bytes: The file content as bytes
        
    Returns:
        bool: True if file has valid PDF signature, False otherwise
    """
    if not file_bytes:
        return False
    
    return file_bytes.startswith(PDF_SIGNATURE)
