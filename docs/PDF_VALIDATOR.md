# Validador de Archivos PDF

## Descripción

Módulo desarrollado con **TDD (Test-Driven Development)** para validar archivos PDF mediante su firma de bytes (file signature).

## ✨ Características

- ✅ Validación de firma de archivo PDF (`%PDF` / `25 50 44 46` hex)
- ✅ Endpoint REST para subir y validar archivos
- ✅ Servicio reutilizable para validación en memoria
- ✅ 100% cobertura de tests

## 🔬 Firma de Archivo PDF

Según [Wikipedia - List of file signatures](https://en.wikipedia.org/wiki/List_of_file_signatures), los archivos PDF válidos deben comenzar con:

- **Bytes Hex**: `25 50 44 46`
- **Texto ASCII**: `%PDF`
- **Offset**: 0 (inicio del archivo)

## 🚀 Uso

### Opción 1: Servicio Python (Programático)

```python
from app.services.file_validator import validate_pdf_signature

# Leer archivo
with open('documento.pdf', 'rb') as f:
    file_bytes = f.read()

# Validar
is_valid = validate_pdf_signature(file_bytes)
print(f"¿Es PDF válido? {is_valid}")
```

### Opción 2: Endpoint REST (API)

```bash
# Validar un archivo PDF
curl -X POST http://localhost:5000/api/files/validate \
  -F "file=@documento.pdf"
```

**Respuesta exitosa (PDF válido):**
```json
{
  "success": true,
  "is_valid": true,
  "file_type": "pdf",
  "filename": "documento.pdf"
}
```

**Respuesta cuando NO es PDF:**
```json
{
  "success": true,
  "is_valid": false,
  "file_type": "unknown",
  "filename": "imagen.png"
}
```

**Respuesta de error:**
```json
{
  "success": false,
  "error": "No file uploaded"
}
```

## 🧪 Tests

### Ejecutar todos los tests:

```bash
# Opción 1: Script batch
run_tests.bat

# Opción 2: Unittest
python -m unittest discover -s tests -p "test_file*.py" -v

# Opción 3: Tests individuales
python tests/test_file_validator.py
python tests/test_file_endpoint.py
```

### Cobertura de Tests

**Servicio (`test_file_validator.py`):**
- ✅ PDF válido con versión 1.4
- ✅ PDF válido con versión 1.7
- ✅ Archivo que no es PDF (PNG)
- ✅ Archivo de texto plano
- ✅ Archivo vacío
- ✅ Firma parcial (incompleta)
- ✅ Firma en medio del archivo

**Endpoint (`test_file_endpoint.py`):**
- ✅ Upload de PDF válido
- ✅ Upload de archivo no-PDF
- ✅ Upload de archivo vacío
- ✅ Request sin archivo
- ✅ Upload de imagen PNG

## 🏗️ Arquitectura (TDD)

```
NotebookUM/
├── app/
│   ├── services/
│   │   └── file_validator.py      # Lógica de validación
│   └── controllers/
│       └── file_controller.py     # Endpoint REST
├── tests/
│   ├── test_file_validator.py     # Tests del servicio
│   └── test_file_endpoint.py      # Tests del endpoint
└── run_tests.bat                  # Script para ejecutar tests
```

## 📋 Desarrollo con TDD

Este módulo fue desarrollado siguiendo el ciclo **Red-Green-Refactor**:

1. 🔴 **RED**: Escribir test que falla
2. 🟢 **GREEN**: Implementar código mínimo para pasar
3. 🔵 **REFACTOR**: Mejorar el código manteniendo tests verdes

### Ciclos TDD aplicados:

1. Test: PDF válido → Implementación: `validate_pdf_signature()`
2. Tests: Casos edge (vacío, parcial, etc.) → Refinamiento validación
3. Tests: Endpoint REST → Implementación: `POST /api/files/validate`
4. Tests: Casos error endpoint → Manejo de errores

## 🔧 Tecnologías

- **Python 3.12+**
- **Flask 3.1.3+**
- **unittest** (testing framework)

## 📝 Notas Técnicas

- La validación solo verifica los primeros 4 bytes (`%PDF`)
- No se valida estructura interna del PDF
- Soporta todas las versiones de PDF (1.0 - 2.0)
- Archivos corruptos con firma válida pasarán la validación

## 🎯 Próximos Pasos (Opcional)

- [ ] Validar también el marcador `%%EOF` al final
- [ ] Detectar otras firmas de archivo (PNG, JPEG, etc.)
- [ ] Agregar límite de tamaño de archivo
- [ ] Validación de estructura interna del PDF
