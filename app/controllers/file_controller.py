from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.services.file_validator import validate_pdf_signature
from app.services.pdf_extractor import extract_pdf_text
from app.utils.exceptions import InvalidPDFException

router = APIRouter(tags=['files'])


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
async def extract_pdf(file: UploadFile | None = File(default=None)):
    """Extract text from an uploaded PDF file."""
    if file is None:
        return JSONResponse(status_code=400, content={
            'success': False,
            'error': 'No file uploaded'
        })

    pdf_bytes = await file.read()

    try:
        extracted_text = extract_pdf_text(pdf_bytes)
        return {
            'success': True,
            'text': extracted_text,
            'length': len(extracted_text),
            'filename': file.filename,
        }
    except InvalidPDFException as exc:
        return JSONResponse(status_code=exc.status, content=exc.to_dict())
