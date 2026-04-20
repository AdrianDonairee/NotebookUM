import unittest
import io
from fastapi.testclient import TestClient
from app import create_app
from src.config import TestingConfig


class TestFileValidationEndpoint(unittest.TestCase):
    """Test suite for the file validation REST endpoint"""
    
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = TestClient(self.app)
    
    def test_upload_valid_pdf_returns_success(self):
        """Test uploading a valid PDF file"""
        # Create a mock PDF file
        pdf_content = b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\nSome PDF content here'
        files = {'file': ('test.pdf', io.BytesIO(pdf_content), 'application/pdf')}
        
        response = self.client.post('/api/files/validate', files=files)
        
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertTrue(json_data['is_valid'])
        self.assertEqual(json_data['file_type'], 'pdf')
    
    def test_upload_invalid_file_returns_failure(self):
        """Test uploading a non-PDF file"""
        # Create a mock text file
        text_content = b'This is not a PDF file'
        files = {'file': ('test.txt', io.BytesIO(text_content), 'text/plain')}
        
        response = self.client.post('/api/files/validate', files=files)
        
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertFalse(json_data['is_valid'])
        self.assertEqual(json_data['file_type'], 'unknown')
    
    def test_upload_empty_file_returns_failure(self):
        """Test uploading an empty file"""
        files = {'file': ('empty.pdf', io.BytesIO(b''), 'application/pdf')}
        
        response = self.client.post('/api/files/validate', files=files)
        
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertFalse(json_data['is_valid'])
    
    def test_no_file_uploaded_returns_error(self):
        """Test request without file"""
        response = self.client.post('/api/files/validate', files={})
        
        self.assertIn(response.status_code, [400, 422])
        json_data = response.json()
        self.assertFalse(json_data['success'])
        self.assertIn('error', json_data)
    
    def test_upload_png_file_returns_invalid(self):
        """Test uploading a PNG file (different signature)"""
        # PNG signature: 89 50 4E 47 0D 0A 1A 0A
        png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00'
        files = {'file': ('image.png', io.BytesIO(png_content), 'image/png')}
        
        response = self.client.post('/api/files/validate', files=files)
        
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertFalse(json_data['is_valid'])


if __name__ == '__main__':
    unittest.main()
