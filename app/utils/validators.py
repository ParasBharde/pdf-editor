"""
Validation utilities for API requests
"""
import json
from werkzeug.datastructures import FileStorage
from app.services.pdf_processor import PDFRedactionService


def validate_file(file: FileStorage) -> dict:
    """
    Validate uploaded file

    Args:
        file: FileStorage object from Flask

    Returns:
        Dictionary with validation result
    """
    if not file:
        return {'valid': False, 'error': 'No file provided'}

    if file.filename == '':
        return {'valid': False, 'error': 'Empty filename'}

    # Check file extension
    if not file.filename.lower().endswith('.pdf'):
        return {'valid': False, 'error': 'Only PDF files are supported'}

    return {'valid': True}


def validate_request_data(form_data, files=None) -> dict:
    """
    Validate request form data

    Args:
        form_data: Form data from Flask request
        files: Files from Flask request (optional)

    Returns:
        Dictionary with validation result and parsed data
    """
    result = {'valid': True}

    # Validate and parse redaction_types
    if 'redaction_types' not in form_data:
        return {'valid': False, 'error': 'redaction_types parameter is required'}

    try:
        redaction_types_str = form_data['redaction_types']

        # Handle both JSON string and plain string
        if isinstance(redaction_types_str, str):
            if redaction_types_str.startswith('['):
                redaction_types = json.loads(redaction_types_str)
            else:
                # Split comma-separated values
                redaction_types = [rt.strip() for rt in redaction_types_str.split(',')]
        else:
            redaction_types = redaction_types_str

        if not isinstance(redaction_types, list) or len(redaction_types) == 0:
            return {'valid': False, 'error': 'redaction_types must be a non-empty list'}

        # Validate redaction types
        if not PDFRedactionService.validate_redaction_types(redaction_types):
            supported = list(PDFRedactionService.SUPPORTED_REDACTION_TYPES.keys())
            return {
                'valid': False,
                'error': f'Invalid redaction type. Supported types: {supported}'
            }

        result['redaction_types'] = redaction_types

    except json.JSONDecodeError:
        return {'valid': False, 'error': 'Invalid JSON format for redaction_types'}
    except Exception as e:
        return {'valid': False, 'error': f'Error parsing redaction_types: {str(e)}'}

    # Validate output_format (optional)
    output_format = form_data.get('output_format', 'pdf')
    if not PDFRedactionService.validate_output_format(output_format):
        supported = PDFRedactionService.SUPPORTED_OUTPUT_FORMATS
        return {
            'valid': False,
            'error': f'Invalid output format. Supported formats: {supported}'
        }
    result['output_format'] = output_format

    # Parse preview flag (optional)
    preview = form_data.get('preview', 'false')
    if isinstance(preview, str):
        result['preview'] = preview.lower() in ['true', '1', 'yes']
    else:
        result['preview'] = bool(preview)

    # Parse use_default_footer flag (optional)
    use_default_footer = form_data.get('use_default_footer', 'false')
    if isinstance(use_default_footer, str):
        result['use_default_footer'] = use_default_footer.lower() in ['true', '1', 'yes']
    else:
        result['use_default_footer'] = bool(use_default_footer)

    # Parse header configuration (optional)
    header_text = form_data.get('header_text')
    if header_text:
        result['header_config'] = {
            'text': header_text,
            'font_size': int(form_data.get('header_font_size', 10)),
            'logo_position': form_data.get('logo_position', 'left')
        }

    # Parse footer configuration (optional)
    footer_text = form_data.get('footer_text')
    if footer_text:
        result['footer_config'] = {
            'text': footer_text,
            'font_size': int(form_data.get('footer_font_size', 9)),
            'align': form_data.get('footer_align', 'center')
        }

    # Parse logo file (optional)
    if files and 'logo' in files:
        logo_file = files['logo']
        if logo_file and logo_file.filename != '':
            # Validate logo file extension
            allowed_extensions = ['png', 'jpg', 'jpeg']
            file_ext = logo_file.filename.rsplit('.', 1)[1].lower() if '.' in logo_file.filename else ''

            if file_ext not in allowed_extensions:
                return {
                    'valid': False,
                    'error': f'Invalid logo file. Supported formats: {allowed_extensions}'
                }

            result['logo_bytes'] = logo_file.read()

    return result
