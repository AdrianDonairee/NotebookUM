import unittest
import io
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import create_app
from config import TestingConfig
from app.models.database import SessionLocal, Usuario, HistorialDocumento, crear_tablas
from app.utils.exceptions import InvalidPDFException


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

class TestPDFExtractPersistenceEndpoint(unittest.TestCase):
    """Integration tests for /api/pdf/extract persistence behavior."""
    GENERIC_USER_EMAIL = "notebookum.generic.user@local"

    @classmethod
    def setUpClass(cls):
        crear_tablas()

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = TestClient(self.app)
        self.db = SessionLocal()

    def tearDown(self):
        try:
            self.db.rollback()
            usuario_generico = self.db.query(Usuario).filter(
                Usuario.email == self.GENERIC_USER_EMAIL
            ).first()
            if usuario_generico is not None:
                self.db.query(HistorialDocumento).filter(
                    HistorialDocumento.usuario_id == usuario_generico.id
                ).delete()
                self.db.delete(usuario_generico)
            self.db.commit()
        except Exception:
            self.db.rollback()
        finally:
            self.db.close()

    @patch("app.controllers.file_controller.extract_pdf_text")
    def test_extract_pdf_saves_extracted_text_in_postgres(self, extract_mock):
        """Valid request saves extracted text in DB and returns success."""
        extract_mock.return_value = "Texto extraido para persistir"
        pdf_content = b'%PDF-1.4\nFake content for endpoint test'
        filename = "persistencia_ok.pdf"

        response = self.client.post(
            "/api/pdf/extract",
            files={"file": (filename, io.BytesIO(pdf_content), "application/pdf")},
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertEqual(body["text"], "Texto extraido para persistir")
        self.assertEqual(body["length"], len("Texto extraido para persistir"))
        self.assertIn("document_id", body)

        documento = self.db.query(HistorialDocumento).filter(
            HistorialDocumento.id == body["document_id"]
        ).first()
        self.assertIsNotNone(documento)
        self.assertEqual(documento.nombre_archivo, filename)
        self.assertEqual(documento.tamaño_bytes, len(pdf_content))
        self.assertEqual(documento.texto_extraido, "Texto extraido para persistir")
        usuario = self.db.query(Usuario).filter(
            Usuario.id == documento.usuario_id
        ).first()
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.email, self.GENERIC_USER_EMAIL)

    @patch("app.controllers.file_controller.extract_pdf_text")
    def test_extract_pdf_without_user_id_still_persists_document(self, extract_mock):
        """Endpoint should persist text without requiring usuario_id in request."""
        extract_mock.return_value = "Texto con usuario generico"

        response = self.client.post(
            "/api/pdf/extract",
            files={"file": ("sin_usuario_id.pdf", io.BytesIO(b"%PDF-1.4\nX"), "application/pdf")},
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertEqual(body["text"], "Texto con usuario generico")
        self.assertIn("document_id", body)

        documento = self.db.query(HistorialDocumento).filter(
            HistorialDocumento.id == body["document_id"]
        ).first()
        self.assertIsNotNone(documento)

    @patch("app.controllers.file_controller.extract_pdf_text")
    def test_extract_pdf_failure_does_not_persist_document(self, extract_mock):
        """If extraction fails, endpoint returns error and no document is saved."""
        extract_mock.side_effect = InvalidPDFException(
            detail="PDF corrupto",
            instance="/api/pdf/extract",
        )

        response = self.client.post(
            "/api/pdf/extract",
            files={"file": ("falla_extraccion.pdf", io.BytesIO(b"%PDF-1.4\nY"), "application/pdf")},
        )

        self.assertEqual(response.status_code, 400)
        body = response.json()
        self.assertEqual(body["detail"], "PDF corrupto")

        documento = self.db.query(HistorialDocumento).filter(
            HistorialDocumento.nombre_archivo == "falla_extraccion.pdf",
        ).first()
        self.assertIsNone(documento)


if __name__ == '__main__':
    unittest.main()
