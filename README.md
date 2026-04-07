# NotebookUM
Programa capaz de resumir y analizar un pdf por medio de un modelo de IA

## 🎯 Nuevas Funcionalidades

### ✅ Validador de Archivos PDF (TDD)
Sistema de validación de archivos PDF mediante firma de bytes (file signature).

**Endpoint:** `POST /api/files/validate`

**Características:**
- Valida firma hexadecimal `25 50 44 46` (%PDF)
- Servicio reutilizable: `validate_pdf_signature()`
- 12 tests unitarios (100% cobertura)
- Desarrollado con TDD (Test-Driven Development)

**Documentación:** Ver [PDF_VALIDATOR.md](PDF_VALIDATOR.md) para detalles completos.

---

# Proyecto NotebookUM
Es un proyecto que tiene como funcionalidades: 
- extraer texto de archivos, utilizando la libreria Docling, 
- El texto extraido debe ser pasado al modelo Nemotron-3 nano 30B para ser resumido.
- El texto resumido va a ser guardado en base de datos.
## Tecnologias utilizadas en el proyecto
Se utilizaran las siguientes tecnologias:
- Metodologia de gestion de proyecto: SCRUM
- Lenguaje: Python (usar PEP8)
- Freamework: FastAPI
- Herramienta de dependencia: uv
- Base de datos: PostgresSQL
- Usar la estructura limpia del proyecto
## Principios
Se aplicaran los siguientes principios:
- KISS
- DRY
- YAGNI
- SOLID
## Metodologias
- TDD
- SDD
## Factor App
Se aplicara los seis primeros factores:
- Codebase
- Dependencias
- Config
- Backing services
- Build, release, run
- Processes
## Diagramas 
- 
## Configuracion de las tablas en base de datos
- 
## Funcionalidad de la base de datos
-
# Especificacion
- Los endpoint debe de empezar con /api/v1
- Deben crearse las siguientes tablas: Usuario, Historial de documentos subidos por usuarios, Historial de preguntas, Resumenes (los nombres de tablas en plural y en minuscula)
- Cada tabla debe tener su CRUD
- Los usuarios envian al archivo endpoint /api/v1/procesar con el metodo POST
- Los archivos validos deben ser contentType: application/pdf y deben ser validados en el servidor, si no son de pdf se manda  en formato json un error 400
- Los archivos no deben superar los 25MB, si superan ese tamaño se manda  en formato json un error status code 400 utilizando rfc9457


