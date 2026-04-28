import unittest
from app.models.database import (
    SessionLocal, Usuario, HistorialDocumento, HistorialPregunta,
    Resumen, crear_tablas, engine
)
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError


class TestDatabaseCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        crear_tablas()

    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        try:
            self.db.rollback()
            self.db.query(Resumen).delete()
            self.db.query(HistorialPregunta).delete()
            self.db.query(HistorialDocumento).delete()
            self.db.query(Usuario).delete()
            self.db.commit()
        except Exception:
            self.db.rollback()
        finally:
            self.db.close()

    def test_postgresql_connection(self):
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            self.assertIsNotNone(result)

    def test_tables_created(self):
        tables = ['usuarios', 'historiales_documentos', 'historiales_preguntas', 'resumenes']
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        with engine.connect() as connection:
            existing = [row[0] for row in connection.execute(text(query))]
            for table in tables:
                self.assertIn(table, existing)

    def test_usuario_crud(self):
        usuario = Usuario(nombre="Juan García", email="juan@test.com", contraseña="pass")
        self.db.add(usuario)
        self.db.commit()
        uid = usuario.id
        user = self.db.query(Usuario).filter(Usuario.id == uid).first()
        self.assertEqual(user.nombre, "Juan García")
        user.nombre = "Juan Actualizado"
        self.db.commit()
        user = self.db.query(Usuario).filter(Usuario.id == uid).first()
        self.assertEqual(user.nombre, "Juan Actualizado")
        self.db.delete(user)
        self.db.commit()
        user = self.db.query(Usuario).filter(Usuario.id == uid).first()
        self.assertIsNone(user)

    def test_usuario_email_unique(self):
        u1 = Usuario(nombre="User 1", email="dup@test.com", contraseña="pass")
        u2 = Usuario(nombre="User 2", email="dup@test.com", contraseña="pass")
        self.db.add(u1)
        self.db.commit()
        self.db.add(u2)
        with self.assertRaises(IntegrityError):
            self.db.commit()

    def test_historial_documento_crud(self):
        usuario = Usuario(nombre="Test User", email="test@test.com", contraseña="pass")
        self.db.add(usuario)
        self.db.commit()
        doc = HistorialDocumento(usuario_id=usuario.id, nombre_archivo="doc.pdf",
                                 ruta_archivo="/uploads/doc.pdf", tamaño_bytes=1024)
        self.db.add(doc)
        self.db.commit()
        did = doc.id
        doc = self.db.query(HistorialDocumento).filter(HistorialDocumento.id == did).first()
        self.assertEqual(doc.nombre_archivo, "doc.pdf")
        doc.nombre_archivo = "doc_updated.pdf"
        self.db.commit()
        self.db.delete(doc)
        self.db.commit()
        doc = self.db.query(HistorialDocumento).filter(HistorialDocumento.id == did).first()
        self.assertIsNone(doc)

    def test_documento_foreign_key(self):
        doc = HistorialDocumento(usuario_id=99999, nombre_archivo="test.pdf",
                                 ruta_archivo="/uploads/test.pdf", tamaño_bytes=1024)
        self.db.add(doc)
        with self.assertRaises(IntegrityError):
            self.db.commit()

    def test_historial_pregunta_crud(self):
        usuario = Usuario(nombre="Test User", email="test2@test.com", contraseña="pass")
        self.db.add(usuario)
        self.db.commit()
        pregunta = HistorialPregunta(usuario_id=usuario.id, pregunta="¿Cuál es el tema?",
                                      respuesta="El tema es...")
        self.db.add(pregunta)
        self.db.commit()
        pid = pregunta.id
        pregunta = self.db.query(HistorialPregunta).filter(HistorialPregunta.id == pid).first()
        self.assertEqual(pregunta.pregunta, "¿Cuál es el tema?")
        pregunta.respuesta = "Nueva respuesta"
        self.db.commit()
        self.db.delete(pregunta)
        self.db.commit()
        pregunta = self.db.query(HistorialPregunta).filter(HistorialPregunta.id == pid).first()
        self.assertIsNone(pregunta)

    def test_resumen_crud(self):
        usuario = Usuario(nombre="Test User", email="test3@test.com", contraseña="pass")
        self.db.add(usuario)
        self.db.commit()
        doc = HistorialDocumento(usuario_id=usuario.id, nombre_archivo="test.pdf",
                                 ruta_archivo="/uploads/test.pdf", tamaño_bytes=1024)
        self.db.add(doc)
        self.db.commit()
        resumen = Resumen(historial_documento_id=doc.id, titulo="Mi Resumen",
                         contenido="Este es el contenido del resumen")
        self.db.add(resumen)
        self.db.commit()
        rid = resumen.id
        resumen = self.db.query(Resumen).filter(Resumen.id == rid).first()
        self.assertEqual(resumen.titulo, "Mi Resumen")
        resumen.contenido = "Contenido actualizado"
        self.db.commit()
        self.db.delete(resumen)
        self.db.commit()
        resumen = self.db.query(Resumen).filter(Resumen.id == rid).first()
        self.assertIsNone(resumen)

    def test_relationships(self):
        usuario = Usuario(nombre="Test User", email="test4@test.com", contraseña="pass")
        self.db.add(usuario)
        self.db.commit()
        doc = HistorialDocumento(usuario_id=usuario.id, nombre_archivo="test.pdf",
                                 ruta_archivo="/uploads/test.pdf", tamaño_bytes=1024)
        self.db.add(doc)
        self.db.commit()
        resumen = Resumen(historial_documento_id=doc.id, titulo="Resumen", contenido="Contenido")
        self.db.add(resumen)
        self.db.commit()
        usuario = self.db.query(Usuario).filter(Usuario.id == usuario.id).first()
        self.assertEqual(len(usuario.historiales_documentos), 1)
        doc = usuario.historiales_documentos[0]
        self.assertEqual(len(doc.resumenes), 1)
        resumen = doc.resumenes[0]
        self.assertEqual(resumen.historial_documento.id, doc.id)


if __name__ == '__main__':
    unittest.main()
