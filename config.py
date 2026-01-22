"""
Configuration settings for PDF Redaction Service
"""
import os

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'temp_uploads')
    ALLOWED_EXTENSIONS = {'pdf'}

    # Redaction settings
    REDACTION_COLOR = (0, 0, 0)  # Black color for redaction boxes
    REDACTION_TEXT = '[REDACTED]'  # Replacement text

    @staticmethod
    def init_app(app):
        # Create upload folder if it doesn't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
