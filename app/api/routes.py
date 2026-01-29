"""
API Routes for PDF Redaction Service
"""
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import io
from app.services.pdf_processor import PDFRedactionService
from app.utils.validators import validate_file, validate_request_data

api_bp = Blueprint('api', __name__)


@api_bp.route('/redact', methods=['POST'])
def redact_pdf():
    """
    Redact sensitive information from PDF

    Expected form data:
    - file: PDF file (required)
    - redaction_types: JSON array of redaction types (required)
      Options: ["email", "phone", "linkedin", "portfolio", "all_urls"]
    - output_format: Output format (optional, default: pdf) Options: ["pdf", "docx"]
    - preview: Boolean to preview what will be redacted (optional, default: false)
    - use_default_footer: Boolean to add Recrui8 footer (optional, default: false)
    - footer_text: Custom footer text (optional)
    - header_text: Custom header text (optional)
    - logo: Logo image file (optional)

    Example request:
    curl -X POST http://localhost:5000/api/redact \
      -F "file=@resume.pdf" \
      -F "redaction_types=[\"email\",\"phone\",\"linkedin\"]" \
      -F "output_format=pdf" \
      -F "use_default_footer=true" \
      -F "logo=@logo.png"
    """
    try:
        # Validate file
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        validation_result = validate_file(file)
        if not validation_result['valid']:
            return jsonify({'error': validation_result['error']}), 400

        # Validate request data
        request_data = validate_request_data(request.form, request.files)
        if not request_data['valid']:
            return jsonify({'error': request_data['error']}), 400

        # Extract parameters
        redaction_types = request_data['redaction_types']
        output_format = request_data.get('output_format', 'pdf')
        preview_mode = request_data.get('preview', False)
        use_default_footer = request_data.get('use_default_footer', False)

        # Get header/footer configuration
        header_config = request_data.get('header_config')
        footer_config = request_data.get('footer_config')
        logo_bytes = request_data.get('logo_bytes')

        # Read PDF file
        pdf_bytes = file.read()

        # Process PDF
        result = PDFRedactionService.process_pdf(
            pdf_bytes=pdf_bytes,
            redaction_types=redaction_types,
            output_format=output_format,
            preview_mode=preview_mode,
            header_config=header_config,
            footer_config=footer_config,
            logo_bytes=logo_bytes,
            use_default_footer=use_default_footer
        )

        # If preview mode, return JSON with detected data
        if preview_mode:
            return jsonify({
                'success': True,
                'preview': True,
                'sensitive_data': result['sensitive_data'],
                'metadata': result['metadata'],
                'message': 'Preview of data that will be redacted'
            }), 200

        # Return redacted document
        redacted_pdf_bytes = result['redacted_pdf']

        # Create filename for download
        original_filename = secure_filename(file.filename) if file.filename else ''
        # Handle case where secure_filename returns empty string
        if not original_filename or original_filename == '.pdf':
            base_name = 'document'
        else:
            base_name = original_filename.rsplit('.', 1)[0]
            # Ensure base_name is not empty
            if not base_name:
                base_name = 'document'
        output_filename = f"{base_name}_redacted.{output_format}"

        # Set MIME type based on output format
        mime_type = 'application/pdf' if output_format == 'pdf' else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

        return send_file(
            io.BytesIO(redacted_pdf_bytes),
            mimetype=mime_type,
            as_attachment=True,
            download_name=output_filename
        ), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to process PDF',
            'details': str(e)
        }), 500


@api_bp.route('/supported-types', methods=['GET'])
def get_supported_types():
    """
    Get list of supported redaction types

    Example request:
    curl http://localhost:5000/api/supported-types
    """
    return jsonify({
        'supported_redaction_types': PDFRedactionService.SUPPORTED_REDACTION_TYPES,
        'supported_output_formats': PDFRedactionService.SUPPORTED_OUTPUT_FORMATS
    }), 200


@api_bp.route('/preview', methods=['POST'])
def preview_redaction():
    """
    Preview what data will be redacted without actually redacting

    Expected form data:
    - file: PDF file (required)
    - redaction_types: JSON array of redaction types (required)

    Example request:
    curl -X POST http://localhost:5000/api/preview \
      -F "file=@resume.pdf" \
      -F "redaction_types=[\"email\",\"phone\"]"
    """
    try:
        # Validate file
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        validation_result = validate_file(file)
        if not validation_result['valid']:
            return jsonify({'error': validation_result['error']}), 400

        # Validate request data
        request_data = validate_request_data(request.form)
        if not request_data['valid']:
            return jsonify({'error': request_data['error']}), 400

        redaction_types = request_data['redaction_types']

        # Read PDF file
        pdf_bytes = file.read()

        # Process PDF in preview mode
        result = PDFRedactionService.process_pdf(
            pdf_bytes=pdf_bytes,
            redaction_types=redaction_types,
            preview_mode=True
        )

        return jsonify({
            'success': True,
            'sensitive_data': result['sensitive_data'],
            'metadata': result['metadata'],
            'redaction_types': result['redaction_types'],
            'message': 'Preview of data that will be redacted'
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to preview PDF',
            'details': str(e)
        }), 500


@api_bp.route('/batch-redact', methods=['POST'])
def batch_redact():
    """
    Redact multiple PDFs at once

    Expected form data:
    - files: Multiple PDF files (required)
    - redaction_types: JSON array of redaction types (required)
    - output_format: Output format (optional, default: pdf)

    Example request:
    curl -X POST http://localhost:5000/api/batch-redact \
      -F "files=@resume1.pdf" \
      -F "files=@resume2.pdf" \
      -F "redaction_types=[\"email\",\"phone\"]"
    """
    try:
        # Validate files
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400

        files = request.files.getlist('files')
        if not files or len(files) == 0:
            return jsonify({'error': 'No files provided'}), 400

        # Validate request data
        request_data = validate_request_data(request.form)
        if not request_data['valid']:
            return jsonify({'error': request_data['error']}), 400

        redaction_types = request_data['redaction_types']
        output_format = request_data.get('output_format', 'pdf')

        results = []
        errors = []

        for file in files:
            try:
                validation_result = validate_file(file)
                if not validation_result['valid']:
                    errors.append({
                        'filename': file.filename,
                        'error': validation_result['error']
                    })
                    continue

                # Read and process PDF
                pdf_bytes = file.read()
                result = PDFRedactionService.process_pdf(
                    pdf_bytes=pdf_bytes,
                    redaction_types=redaction_types,
                    output_format=output_format
                )

                results.append({
                    'filename': secure_filename(file.filename),
                    'redacted_count': result['sensitive_data_redacted'],
                    'success': True
                })

            except Exception as e:
                errors.append({
                    'filename': file.filename,
                    'error': str(e)
                })

        return jsonify({
            'success': True,
            'processed': len(results),
            'errors': len(errors),
            'results': results,
            'error_details': errors
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to process batch',
            'details': str(e)
        }), 500
