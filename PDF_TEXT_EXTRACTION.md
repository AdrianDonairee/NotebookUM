# PDF Text Extraction - Guía de Uso

## Descripción

Servicio para extraer texto de archivos PDF usando la librería docling 2.85. El servicio trabaja completamente con arrays de bytes en memoria, sin necesidad de guardar archivos temporales.

## Características

- ✅ Validación de firma PDF usando `validate_pdf_signature()`
- ✅ Extracción de texto usando docling 2.85
- ✅ Procesamiento en memoria (sin archivos temporales)
- ✅ Soporte para PDFs multipágina
- ✅ Manejo de errores con RFC 9457 Problem Details
- ✅ Cobertura completa de tests

## Instalación

La librería docling ya está instalada en el proyecto:

```bash
# Ver pyproject.toml
docling==2.85.0
```

## Uso Básico

```python
from app.services.pdf_extractor import extract_pdf_text
from app.utils.exceptions import InvalidPDFException

# Leer PDF desde archivo
with open('documento.pdf', 'rb') as f:
    pdf_bytes = f.read()

try:
    # Extraer texto
    texto = extract_pdf_text(pdf_bytes)
    print(f"Texto extraído ({len(texto)} caracteres):")
    print(texto)
    
except InvalidPDFException as e:
    # Manejo de errores RFC 9457
    print(f"Error {e.status}: {e.title}")
    print(f"Detalle: {e.detail}")
    print(f"Tipo: {e.type_uri}")
```

## Uso con Flask/API

```python
from flask import Flask, request, jsonify
from app.services.pdf_extractor import extract_pdf_text
from app.utils.exceptions import InvalidPDFException

app = Flask(__name__)

@app.route('/api/pdf/extract', methods=['POST'])
def extract_pdf_text_endpoint():
    """Endpoint para extraer texto de PDF"""
    
    # Obtener archivo del request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    pdf_bytes = file.read()
    
    try:
        # Extraer texto
        text = extract_pdf_text(pdf_bytes)
        
        return jsonify({
            'success': True,
            'text': text,
            'length': len(text)
        }), 200
        
    except InvalidPDFException as e:
        # Retornar error en formato RFC 9457
        return jsonify(e.to_dict()), e.status
```

## Manejo de Errores

El servicio utiliza excepciones RFC 9457 para errores estructurados:

### InvalidPDFException

```python
{
    "type": "https://notebookum.com/problems/invalid-pdf",
    "title": "Invalid PDF File",
    "status": 400,
    "detail": "The provided file does not have a valid PDF signature",
    "instance": "/api/pdf/extract"
}
```

### Casos de Error

1. **Archivo vacío**:
   ```python
   extract_pdf_text(b"")
   # Lanza: InvalidPDFException("Cannot extract text from empty file")
   ```

2. **Firma PDF inválida**:
   ```python
   extract_pdf_text(b"Not a PDF")
   # Lanza: InvalidPDFException("The provided file does not have a valid PDF signature")
   ```

3. **Error de procesamiento docling**:
   ```python
   extract_pdf_text(corrupted_pdf_bytes)
   # Lanza: InvalidPDFException("Failed to extract text from PDF: ...")
   ```

## Arquitectura

### Flujo de Procesamiento

```
pdf_bytes (bytes)
    ↓
[Validación de firma PDF]
    ↓
[Crear BytesIO stream]
    ↓
[docling DocumentConverter]
    ↓
[Extraer texto]
    ↓
texto (str)
```

### Integración con file_validator

El servicio utiliza `validate_pdf_signature()` del módulo `file_validator.py`:

```python
from app.services.file_validator import validate_pdf_signature

# Validación de firma (bytes 0-3 deben ser %PDF)
if not validate_pdf_signature(pdf_bytes):
    raise InvalidPDFException(...)
```

## Tests

Los tests cubren todos los casos de uso:

```bash
# Ejecutar tests
python tests\test_pdf_extractor.py
python tests\test_rfc9457_exceptions.py
```

### Casos Probados

1. ✅ PDF válido con texto → extrae correctamente
2. ✅ PDF inválido → lanza InvalidPDFException
3. ✅ Bytes vacíos → lanza InvalidPDFException
4. ✅ PDF sin texto → retorna cadena vacía
5. ✅ PDF multipágina → extrae todo el texto

## Principios de Diseño

### SOLID

- **Single Responsibility**: `extract_pdf_text()` solo extrae texto, `_validate_pdf_bytes()` solo valida
- **Open/Closed**: Extensible para nuevos tipos de excepciones RFC 9457
- **Liskov Substitution**: `InvalidPDFException` es intercambiable con `ProblemDetailException`
- **Interface Segregation**: Interfaz mínima y clara (`pdf_bytes -> str`)
- **Dependency Inversion**: Depende de abstracciones (docling, file_validator)

### Clean Code

- Nombres descriptivos (`extract_pdf_text`, `_validate_pdf_bytes`)
- Funciones pequeñas y enfocadas
- Sin duplicación de código (DRY)
- Comentarios solo donde agregan valor
- Constantes extraídas (`_EXTRACTION_ENDPOINT`)

## Limitaciones Conocidas

- Requiere que el PDF tenga texto extraíble (no funciona con PDFs escaneados sin OCR)
- Depende de la capacidad de docling para procesar el PDF
- El formato del texto extraído depende de docling

## Próximos Pasos

Posibles mejoras futuras:

- [ ] Soporte para OCR en PDFs escaneados
- [ ] Opciones de formato de salida (markdown, HTML, etc.)
- [ ] Extracción de metadatos del PDF
- [ ] Procesamiento por páginas específicas
- [ ] Cache de resultados para PDFs grandes

## Referencias

- [RFC 9457 - Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
- [docling Documentation](https://github.com/DS4SD/docling)
- [PDF File Signature Specification](https://en.wikipedia.org/wiki/List_of_file_signatures)
