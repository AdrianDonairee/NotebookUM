import unittest
from app.services.file_validator import validate_pdf_signature


class TestPDFSignatureValidation(unittest.TestCase):
    """Test suite for PDF file signature validation"""
    
    def test_valid_pdf_returns_true(self):
        """Test that a valid PDF file returns True"""
        # PDF signature: %PDF in hex is 25 50 44 46
        valid_pdf_bytes = b'%PDF-1.4\n'
        result = validate_pdf_signature(valid_pdf_bytes)
        self.assertTrue(result)
    
    def test_valid_pdf_with_version_1_7(self):
        """Test that PDF with version 1.7 is valid"""
        valid_pdf_bytes = b'%PDF-1.7\n%\xe2\xe3\xcf\xd3\n'
        result = validate_pdf_signature(valid_pdf_bytes)
        self.assertTrue(result)
    
    def test_non_pdf_file_returns_false(self):
        """Test that a non-PDF file returns False"""
        # PNG signature
        png_bytes = b'\x89PNG\r\n\x1a\n'
        result = validate_pdf_signature(png_bytes)
        self.assertFalse(result)
    
    def test_text_file_returns_false(self):
        """Test that a plain text file returns False"""
        text_bytes = b'This is a text file, not a PDF'
        result = validate_pdf_signature(text_bytes)
        self.assertFalse(result)
    
    def test_empty_file_returns_false(self):
        """Test that an empty file returns False"""
        empty_bytes = b''
        result = validate_pdf_signature(empty_bytes)
        self.assertFalse(result)
    
    def test_partial_signature_returns_false(self):
        """Test that a file with partial PDF signature returns False"""
        partial_bytes = b'%PD'  # Only 3 bytes instead of 4
        result = validate_pdf_signature(partial_bytes)
        self.assertFalse(result)
    
    def test_signature_in_middle_returns_false(self):
        """Test that PDF signature in the middle of file returns False"""
        # Signature must be at offset 0
        middle_sig_bytes = b'HEADER%PDF-1.4'
        result = validate_pdf_signature(middle_sig_bytes)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
