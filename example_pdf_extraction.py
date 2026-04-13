"""
Ejemplo completo de uso del servicio de extracción de texto de PDF.

Este script demuestra cómo usar extract_pdf_text() para procesar PDFs
sin guardar archivos temporales.
"""

import sys
sys.path.insert(0, r'C:\Users\anchi\OneDrive\Escritorio\Facultad\4to\Ingenieria de software\NotebookUM')

from app.services.pdf_extractor import extract_pdf_text
from app.utils.exceptions import InvalidPDFException


def ejemplo_basico():
    """Ejemplo 1: Uso básico con un PDF válido"""
    print("=" * 60)
    print("EJEMPLO 1: Extracción básica de texto")
    print("=" * 60)
    
    # Crear un PDF mínimo válido para demostración
    pdf_minimo = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 50
>>
stream
BT
/F1 12 Tf
100 700 Td
(Hola Mundo PDF) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000317 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
420
%%EOF"""
    
    try:
        texto = extract_pdf_text(pdf_minimo)
        print(f"✓ Texto extraído exitosamente")
        print(f"  Longitud: {len(texto)} caracteres")
        print(f"  Contenido: {texto[:100]}...")
    except InvalidPDFException as e:
        print(f"✗ Error: {e.detail}")
        print(f"  Estructura RFC 9457:")
        for key, value in e.to_dict().items():
            print(f"    {key}: {value}")


def ejemplo_manejo_errores():
    """Ejemplo 2: Manejo de errores con RFC 9457"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Manejo de errores")
    print("=" * 60)
    
    casos_de_error = [
        ("Archivo vacío", b""),
        ("Firma inválida", b"Este no es un PDF"),
        ("Bytes incorrectos", b"\x00\x01\x02\x03")
    ]
    
    for nombre, pdf_bytes in casos_de_error:
        print(f"\nProbando: {nombre}")
        try:
            texto = extract_pdf_text(pdf_bytes)
            print(f"  ✗ No debería llegar aquí")
        except InvalidPDFException as e:
            print(f"  ✓ InvalidPDFException capturada")
            print(f"    Status: {e.status}")
            print(f"    Title: {e.title}")
            print(f"    Detail: {e.detail}")
            print(f"    Type URI: {e.type_uri}")


def ejemplo_integracion_flask():
    """Ejemplo 3: Estructura para integración con Flask"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Patrón de integración con Flask")
    print("=" * 60)
    
    print("""
# Código de ejemplo para Flask endpoint:

from flask import Flask, request, jsonify
from app.services.pdf_extractor import extract_pdf_text
from app.utils.exceptions import InvalidPDFException

app = Flask(__name__)

@app.route('/api/pdf/extract', methods=['POST'])
def extract_text_endpoint():
    '''Endpoint para extraer texto de PDF uploadido'''
    
    # Validar que se envió un archivo
    if 'file' not in request.files:
        return jsonify({
            'type': 'https://notebookum.com/problems/missing-file',
            'title': 'Missing File',
            'status': 400,
            'detail': 'No file was provided in the request'
        }), 400
    
    # Leer archivo en memoria (sin guardar)
    file = request.files['file']
    pdf_bytes = file.read()
    
    try:
        # Extraer texto del PDF
        text = extract_pdf_text(pdf_bytes)
        
        # Respuesta exitosa
        return jsonify({
            'success': True,
            'filename': file.filename,
            'text': text,
            'char_count': len(text),
            'word_count': len(text.split())
        }), 200
        
    except InvalidPDFException as e:
        # Retornar error en formato RFC 9457
        return jsonify(e.to_dict()), e.status

if __name__ == '__main__':
    app.run(debug=True)
    
# Uso con curl:
# curl -X POST -F "file=@documento.pdf" http://localhost:5000/api/pdf/extract
    """)


def ejemplo_procesamiento_batch():
    """Ejemplo 4: Procesar múltiples PDFs"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Procesamiento batch de PDFs")
    print("=" * 60)
    
    print("""
# Código de ejemplo para procesar múltiples PDFs:

from pathlib import Path
from app.services.pdf_extractor import extract_pdf_text
from app.utils.exceptions import InvalidPDFException

def procesar_directorio_pdfs(directorio: str) -> dict:
    '''Procesa todos los PDFs en un directorio'''
    
    resultados = {
        'exitosos': [],
        'fallidos': []
    }
    
    # Buscar todos los archivos PDF
    ruta = Path(directorio)
    archivos_pdf = list(ruta.glob('**/*.pdf'))
    
    print(f"Encontrados {len(archivos_pdf)} archivos PDF")
    
    for archivo in archivos_pdf:
        print(f"Procesando: {archivo.name}...")
        
        try:
            # Leer PDF en memoria
            with open(archivo, 'rb') as f:
                pdf_bytes = f.read()
            
            # Extraer texto
            texto = extract_pdf_text(pdf_bytes)
            
            # Guardar resultado
            resultados['exitosos'].append({
                'archivo': archivo.name,
                'ruta': str(archivo),
                'texto': texto,
                'caracteres': len(texto)
            })
            
            print(f"  ✓ Extraídos {len(texto)} caracteres")
            
        except InvalidPDFException as e:
            resultados['fallidos'].append({
                'archivo': archivo.name,
                'ruta': str(archivo),
                'error': e.detail,
                'status': e.status
            })
            print(f"  ✗ Error: {e.detail}")
    
    return resultados

# Uso:
# resultados = procesar_directorio_pdfs('./documentos')
# print(f"Exitosos: {len(resultados['exitosos'])}")
# print(f"Fallidos: {len(resultados['fallidos'])}")
    """)


if __name__ == '__main__':
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "EJEMPLOS DE USO: PDF TEXT EXTRACTOR" + " " * 12 + "║")
    print("╚" + "═" * 58 + "╝")
    
    ejemplo_basico()
    ejemplo_manejo_errores()
    ejemplo_integracion_flask()
    ejemplo_procesamiento_batch()
    
    print("\n" + "=" * 60)
    print("✅ Todos los ejemplos completados")
    print("=" * 60)
    print("\nPara más información, ver: PDF_TEXT_EXTRACTION.md")
