"""
PDF Redaction Microservice
Main application entry point
"""
import os
from flask import Flask
from flask_cors import CORS
from app.api.routes import api_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for integration with MERN frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'service': 'pdf-redaction-service'}, 200

    return app

# Create app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
