import unittest

from fastapi.testclient import TestClient
from pydantic import ValidationError

from app import create_app
from config import TestingConfig


class TestFunctionalityCreate(unittest.TestCase):
    """Tests para la creación de funcionalidades (POST)"""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = TestClient(self.app)

    def test_create_functionality_success(self):
        """Debe crear una funcionalidad con éxito"""
        response = self.client.post(
            "/api/v1/funcionalidades/",
            json={"name": "Extraer texto", "description": "Usa docling"},
        )
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertIn("data", body)

        data = body["data"]
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Extraer texto")
        self.assertEqual(data["description"], "Usa docling")

    def test_create_with_empty_description(self):
        """Debe crear funcionalidad con descripción vacía"""
        response = self.client.post(
            "/api/v1/funcionalidades/",
            json={"name": "Procesar documento"},
        )
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertEqual(body["data"]["description"], "")

    def test_create_generates_incremental_ids(self):
        """Debe generar IDs incrementales"""
        # Crear primer item
        response1 = self.client.post(
            "/api/v1/funcionalidades/",
            json={"name": "Función 1"},
        )
        id1 = response1.json()["data"]["id"]

        # Crear segundo item
        response2 = self.client.post(
            "/api/v1/funcionalidades/",
            json={"name": "Función 2"},
        )
        id2 = response2.json()["data"]["id"]

        # Los IDs deben ser diferentes e incrementales
        self.assertNotEqual(id1, id2)
        self.assertGreater(id2, id1)

    def test_create_missing_name_fails(self):
        """Debe fallar si falta el nombre"""
        response = self.client.post(
            "/api/v1/funcionalidades/",
            json={"description": "Sin nombre"},
        )
        self.assertEqual(response.status_code, 422)

    def test_create_empty_name_fails(self):
        """Debe fallar si el nombre está vacío"""
        response = self.client.post(
            "/api/v1/funcionalidades/",
            json={"name": "", "description": "Nombre vacío"},
        )
        self.assertEqual(response.status_code, 422)

    def test_create_response_contains_success_flag(self):
        """La respuesta debe contener el flag 'success'"""
        response = self.client.post(
            "/api/v1/funcionalidades/",
            json={"name": "Test"},
        )
        body = response.json()
        self.assertIn("success", body)
        self.assertTrue(body["success"])


class TestFunctionalityRead(unittest.TestCase):
    """Tests para lectura de funcionalidades (GET)"""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = TestClient(self.app)
        # Crear datos de prueba
        self.response = self.client.post(
            "/api/v1/funcionalidades/",
            json={"name": "Extraer texto", "description": "Usa docling"},
        )
        self.created_id = self.response.json()["data"]["id"]

    def test_get_all_functionalities(self):
        """Debe retornar todas las funcionalidades"""
        response = self.client.get("/api/v1/funcionalidades/")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertIsInstance(body["data"], list)
        self.assertGreaterEqual(len(body["data"]), 1)

    def test_get_all_empty_list(self):
        """Debe retornar lista vacía cuando no hay items"""
        response = self.client.get("/api/v1/funcionalidades/")
        body = response.json()
        self.assertIsInstance(body["data"], list)

    def test_get_functionality_by_id(self):
        """Debe retornar una funcionalidad específica por ID"""
        response = self.client.get(f"/api/v1/funcionalidades/{self.created_id}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertEqual(body["data"]["id"], self.created_id)
        self.assertEqual(body["data"]["name"], "Extraer texto")

    def test_get_nonexistent_functionality(self):
        """Debe retornar 404 para ID inexistente"""
        response = self.client.get("/api/v1/funcionalidades/999")
        self.assertEqual(response.status_code, 404)
        body = response.json()
        self.assertFalse(body["success"])
        self.assertIn("message", body)


class TestFunctionalityUpdate(unittest.TestCase):
    """Tests para actualización de funcionalidades (PUT)"""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = TestClient(self.app)
        # Crear funcionalidad de prueba
        response = self.client.post(
            "/api/v1/funcionalidades/",
            json={"name": "Original", "description": "Descripción original"},
        )
        self.functionality_id = response.json()["data"]["id"]

    def test_update_name_only(self):
        """Debe actualizar solo el nombre"""
        response = self.client.put(
            f"/api/v1/funcionalidades/{self.functionality_id}",
            json={"name": "Actualizado"},
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertEqual(body["data"]["name"], "Actualizado")
        self.assertEqual(body["data"]["description"], "Descripción original")

    def test_update_description_only(self):
        """Debe actualizar solo la descripción"""
        response = self.client.put(
            f"/api/v1/funcionalidades/{self.functionality_id}",
            json={"description": "Nueva descripción"},
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertEqual(body["data"]["name"], "Original")
        self.assertEqual(body["data"]["description"], "Nueva descripción")

    def test_update_both_fields(self):
        """Debe actualizar nombre y descripción"""
        response = self.client.put(
            f"/api/v1/funcionalidades/{self.functionality_id}",
            json={"name": "Nuevo nombre", "description": "Nueva descripción"},
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["data"]["name"], "Nuevo nombre")
        self.assertEqual(body["data"]["description"], "Nueva descripción")

    def test_update_persistence(self):
        """Los cambios deben persistir en lecturas posteriores"""
        self.client.put(
            f"/api/v1/funcionalidades/{self.functionality_id}",
            json={"name": "Persistido"},
        )
        response = self.client.get(f"/api/v1/funcionalidades/{self.functionality_id}")
        body = response.json()
        self.assertEqual(body["data"]["name"], "Persistido")

    def test_update_nonexistent_functionality(self):
        """Debe retornar 404 al actualizar ID inexistente"""
        response = self.client.put(
            "/api/v1/funcionalidades/999",
            json={"name": "No existe"},
        )
        self.assertEqual(response.status_code, 404)
        body = response.json()
        self.assertFalse(body["success"])

    def test_update_empty_name_fails(self):
        """Debe fallar si se intenta actualizar con nombre vacío"""
        response = self.client.put(
            f"/api/v1/funcionalidades/{self.functionality_id}",
            json={"name": ""},
        )
        self.assertEqual(response.status_code, 422)

    def test_update_with_empty_description_allowed(self):
        """Debe permitir actualizar descripción a vacío"""
        response = self.client.put(
            f"/api/v1/funcionalidades/{self.functionality_id}",
            json={"description": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["description"], "")


class TestFunctionalityDelete(unittest.TestCase):
    """Tests para eliminación de funcionalidades (DELETE)"""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = TestClient(self.app)
        # Crear funcionalidad de prueba
        response = self.client.post(
            "/api/v1/funcionalidades/",
            json={"name": "A eliminar"},
        )
        self.functionality_id = response.json()["data"]["id"]

    def test_delete_functionality_success(self):
        """Debe eliminar una funcionalidad existente"""
        response = self.client.delete(
            f"/api/v1/funcionalidades/{self.functionality_id}"
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertIn("message", body)

    def test_delete_makes_item_inaccessible(self):
        """El item debe ser inaccesible después de eliminarlo"""
        self.client.delete(f"/api/v1/funcionalidades/{self.functionality_id}")
        response = self.client.get(f"/api/v1/funcionalidades/{self.functionality_id}")
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_functionality(self):
        """Debe retornar 404 al eliminar ID inexistente"""
        response = self.client.delete("/api/v1/funcionalidades/999")
        self.assertEqual(response.status_code, 404)
        body = response.json()
        self.assertFalse(body["success"])

    def test_delete_removes_from_list(self):
        """El item no debe aparecer en listados después de eliminarlo"""
        # Obtener count inicial
        response_before = self.client.get("/api/v1/funcionalidades/")
        count_before = len(response_before.json()["data"])

        # Eliminar
        self.client.delete(f"/api/v1/funcionalidades/{self.functionality_id}")

        # Verificar count final
        response_after = self.client.get("/api/v1/funcionalidades/")
        count_after = len(response_after.json()["data"])
        self.assertEqual(count_after, count_before - 1)


class TestFunctionalityIntegration(unittest.TestCase):
    """Tests de integración - flujo completo CRUD"""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = TestClient(self.app)

    def test_complete_crud_flow(self):
        """Debe permitir el flujo completo: crear, leer, actualizar, eliminar"""
        # CREATE
        create_response = self.client.post(
            "/api/v1/funcionalidades/",
            json={"name": "Extraer texto", "description": "Usa docling"},
        )
        self.assertEqual(create_response.status_code, 201)
        created = create_response.json()["data"]
        functionality_id = created["id"]

        # READ (all)
        get_all_response = self.client.get("/api/v1/funcionalidades/")
        self.assertEqual(get_all_response.status_code, 200)
        self.assertGreaterEqual(len(get_all_response.json()["data"]), 1)

        # READ (one)
        get_one_response = self.client.get(
            f"/api/v1/funcionalidades/{functionality_id}"
        )
        self.assertEqual(get_one_response.status_code, 200)
        self.assertEqual(get_one_response.json()["data"]["name"], "Extraer texto")

        # UPDATE
        update_response = self.client.put(
            f"/api/v1/funcionalidades/{functionality_id}",
            json={"description": "Extrae contenido PDF y lo prepara para resumen"},
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(
            update_response.json()["data"]["description"],
            "Extrae contenido PDF y lo prepara para resumen",
        )

        # DELETE
        delete_response = self.client.delete(
            f"/api/v1/funcionalidades/{functionality_id}"
        )
        self.assertEqual(delete_response.status_code, 200)

        # VERIFY DELETION
        get_deleted_response = self.client.get(
            f"/api/v1/funcionalidades/{functionality_id}"
        )
        self.assertEqual(get_deleted_response.status_code, 404)

    def test_multiple_items_crud(self):
        """Debe manejar correctamente múltiples items"""
        # Crear 3 items
        ids = []
        for i in range(3):
            response = self.client.post(
                "/api/v1/funcionalidades/",
                json={"name": f"Funcionalidad {i+1}"},
            )
            ids.append(response.json()["data"]["id"])

        # Verificar que todos existen
        get_all = self.client.get("/api/v1/funcionalidades/")
        self.assertGreaterEqual(len(get_all.json()["data"]), 3)

        # Eliminar el segundo
        self.client.delete(f"/api/v1/funcionalidades/{ids[1]}")

        # Verificar que los otros 2 siguen existiendo
        response1 = self.client.get(f"/api/v1/funcionalidades/{ids[0]}")
        response2 = self.client.get(f"/api/v1/funcionalidades/{ids[2]}")
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

        # Verificar que el eliminado no existe
        response_deleted = self.client.get(f"/api/v1/funcionalidades/{ids[1]}")
        self.assertEqual(response_deleted.status_code, 404)


if __name__ == "__main__":
    unittest.main()
