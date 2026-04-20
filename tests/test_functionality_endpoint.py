import unittest

from fastapi.testclient import TestClient

from app import create_app
from src.config import TestingConfig


class TestFunctionalityEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = TestClient(self.app)

    def test_crud_flow(self):
        create_response = self.client.post(
            "/api/v1/funcionalidades/",
            json={"name": "Extraer texto", "description": "Usa docling"},
        )
        self.assertEqual(create_response.status_code, 201)
        create_body = create_response.json()
        self.assertTrue(create_body["success"])
        created = create_body["data"]
        self.assertEqual(created["id"], 1)
        self.assertEqual(created["name"], "Extraer texto")

        get_all_response = self.client.get("/api/v1/funcionalidades/")
        self.assertEqual(get_all_response.status_code, 200)
        get_all_body = get_all_response.json()
        self.assertTrue(get_all_body["success"])
        self.assertEqual(len(get_all_body["data"]), 1)

        functionality_id = created["id"]
        get_one_response = self.client.get(f"/api/v1/funcionalidades/{functionality_id}")
        self.assertEqual(get_one_response.status_code, 200)
        get_one_body = get_one_response.json()
        self.assertTrue(get_one_body["success"])
        self.assertEqual(get_one_body["data"]["name"], "Extraer texto")

        update_response = self.client.put(
            f"/api/v1/funcionalidades/{functionality_id}",
            json={"description": "Extrae contenido PDF y lo prepara para resumen"},
        )
        self.assertEqual(update_response.status_code, 200)
        update_body = update_response.json()
        self.assertTrue(update_body["success"])
        self.assertEqual(
            update_body["data"]["description"],
            "Extrae contenido PDF y lo prepara para resumen",
        )

        delete_response = self.client.delete(
            f"/api/v1/funcionalidades/{functionality_id}"
        )
        self.assertEqual(delete_response.status_code, 200)
        delete_body = delete_response.json()
        self.assertTrue(delete_body["success"])

        get_deleted_response = self.client.get(
            f"/api/v1/funcionalidades/{functionality_id}"
        )
        self.assertEqual(get_deleted_response.status_code, 404)

    def test_not_found_cases(self):
        get_response = self.client.get("/api/v1/funcionalidades/999")
        self.assertEqual(get_response.status_code, 404)

        update_response = self.client.put(
            "/api/v1/funcionalidades/999",
            json={"name": "No existe"},
        )
        self.assertEqual(update_response.status_code, 404)

        delete_response = self.client.delete("/api/v1/funcionalidades/999")
        self.assertEqual(delete_response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
