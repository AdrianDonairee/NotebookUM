import unittest
from fastapi.testclient import TestClient
from app import create_app
from src.config import TestingConfig

class TestExample(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = TestClient(self.app)
    
    def test_get_all(self):
        response = self.client.get('/api/example/')
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
    
if __name__ == '__main__':
    unittest.main()