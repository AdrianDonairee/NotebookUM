"""
Ejemplo de uso del validador de PDF
Ejecutar: python example_usage.py
"""

from app.services.file_validator import validate_pdf_signature


def main():
    print("=" * 60)
    print("Ejemplo: Validador de Firma de Archivos PDF")
    print("=" * 60)
    print()
    
    # Ejemplo 1: PDF válido
    print("1. Probando con contenido PDF válido:")
    pdf_bytes = b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\nContenido del PDF...'
    result = validate_pdf_signature(pdf_bytes)
    print(f"   Bytes: {pdf_bytes[:20]}...")
    print(f"   ¿Es PDF válido? {result}")
    print(f"   ✓ Resultado correcto" if result else "   ✗ Error inesperado")
    print()
    
    # Ejemplo 2: Archivo que no es PDF
    print("2. Probando con archivo de texto:")
    text_bytes = b'Este es un archivo de texto, no PDF'
    result = validate_pdf_signature(text_bytes)
    print(f"   Bytes: {text_bytes[:20]}...")
    print(f"   ¿Es PDF válido? {result}")
    print(f"   ✓ Resultado correcto" if not result else "   ✗ Error inesperado")
    print()
    
    # Ejemplo 3: Archivo PNG
    print("3. Probando con archivo PNG:")
    png_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
    result = validate_pdf_signature(png_bytes)
    print(f"   Bytes (hex): {png_bytes[:8].hex()}")
    print(f"   ¿Es PDF válido? {result}")
    print(f"   ✓ Resultado correcto" if not result else "   ✗ Error inesperado")
    print()
    
    # Ejemplo 4: Archivo vacío
    print("4. Probando con archivo vacío:")
    empty_bytes = b''
    result = validate_pdf_signature(empty_bytes)
    print(f"   Bytes: (vacío)")
    print(f"   ¿Es PDF válido? {result}")
    print(f"   ✓ Resultado correcto" if not result else "   ✗ Error inesperado")
    print()
    
    # Ejemplo 5: Firma parcial
    print("5. Probando con firma parcial:")
    partial_bytes = b'%PD'
    result = validate_pdf_signature(partial_bytes)
    print(f"   Bytes: {partial_bytes}")
    print(f"   ¿Es PDF válido? {result}")
    print(f"   ✓ Resultado correcto" if not result else "   ✗ Error inesperado")
    print()
    
    print("=" * 60)
    print("Firma de PDF esperada (Wikipedia):")
    print("  Hex: 25 50 44 46")
    print("  ASCII: %PDF")
    print("  URL: https://en.wikipedia.org/wiki/List_of_file_signatures")
    print("=" * 60)


if __name__ == '__main__':
    main()
