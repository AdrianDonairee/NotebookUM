from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.database import HistorialDocumento, Usuario, obtener_sesion_db
from app.services.file_validator import validate_pdf_signature
from app.services.pdf_extractor import extract_pdf_text
from app.utils.exceptions import InvalidPDFException

router = APIRouter(tags=['files'])
_GENERIC_USER_EMAIL = "notebookum.generic.user@local"
_GENERIC_USER_NAME = "Usuario Generico"
_GENERIC_USER_PASSWORD = "notebookum_generic_password"


def _build_document_history(
    usuario_id: int,
    file_name: str | None,
    pdf_bytes: bytes,
    extracted_text: str,
) -> HistorialDocumento:
    nombre_archivo = file_name or "archivo.pdf"
    return HistorialDocumento(
        usuario_id=usuario_id,
        nombre_archivo=nombre_archivo,
        ruta_archivo=nombre_archivo,
        tamaño_bytes=len(pdf_bytes),
        texto_extraido=extracted_text,
    )


def _get_or_create_generic_user(db: Session) -> Usuario:
    usuario_generico = db.query(Usuario).filter(
        Usuario.email == _GENERIC_USER_EMAIL
    ).first()
    if usuario_generico is not None:
        return usuario_generico

    usuario_generico = Usuario(
        nombre=_GENERIC_USER_NAME,
        email=_GENERIC_USER_EMAIL,
        contraseña=_GENERIC_USER_PASSWORD,
    )
    db.add(usuario_generico)
    db.commit()
    db.refresh(usuario_generico)
    return usuario_generico


@router.post('/api/files/validate')
async def validate_file(file: UploadFile | None = File(default=None)):
    """
    Endpoint para validar si un archivo subido es un PDF válido.
    
    Expects:
        - multipart/form-data with a 'file' field
    
    Returns:
        JSON with:
        - success: bool
        - is_valid: bool (if file was uploaded)
        - file_type: str ('pdf' or 'unknown')
        - error: str (if error occurred)
    """
    if file is None:
        return JSONResponse(status_code=400, content={
            'success': False,
            'error': 'No file uploaded'
        })
    
    # Check if file is empty
    if not file.filename:
        return JSONResponse(status_code=400, content={
            'success': False,
            'error': 'No file selected'
        })
    
    # Read file content
    file_content = await file.read()
    
    # Validate PDF signature
    is_valid_pdf = validate_pdf_signature(file_content)
    
    return {
        'success': True,
        'is_valid': is_valid_pdf,
        'file_type': 'pdf' if is_valid_pdf else 'unknown',
        'filename': file.filename
    }


@router.post('/api/pdf/extract')
async def extract_pdf(
    file: UploadFile | None = File(default=None),
    db: Session = Depends(obtener_sesion_db),
):
    """Extract text from an uploaded PDF file and persist it for a generic user."""
    if file is None:
        return JSONResponse(status_code=400, content={
            'success': False,
            'error': 'No file uploaded'
        })

    pdf_bytes = await file.read()

    try:
        usuario_generico = _get_or_create_generic_user(db)
        extracted_text = extract_pdf_text(pdf_bytes)
        historial = _build_document_history(
            usuario_id=usuario_generico.id,
            file_name=file.filename,
            pdf_bytes=pdf_bytes,
            extracted_text=extracted_text,
        )
        db.add(historial)
        db.commit()
        db.refresh(historial)
        return {
            'success': True,
            'text': extracted_text,
            'length': len(extracted_text),
            'filename': file.filename,
            'document_id': historial.id,
        }
    except InvalidPDFException as exc:
        return JSONResponse(status_code=exc.status, content=exc.to_dict())
