from flask import Blueprint, request, jsonify
from app.services.file_validator import validate_pdf_signature

file_bp = Blueprint('files', __name__, url_prefix='/api/files')


@file_bp.route('/validate', methods=['POST'])
def validate_file():
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
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file uploaded'
        }), 400
    
    file = request.files['file']
    
    # Check if file is empty
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400
    
    # Read file content
    file_content = file.read()
    
    # Validate PDF signature
    is_valid_pdf = validate_pdf_signature(file_content)
    
    return jsonify({
        'success': True,
        'is_valid': is_valid_pdf,
        'file_type': 'pdf' if is_valid_pdf else 'unknown',
        'filename': file.filename
    }), 200
