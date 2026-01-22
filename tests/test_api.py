"""
API endpoint tests
"""
import pytest
import io
from app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'pdf-redaction-service'


def test_supported_types(client):
    """Test supported types endpoint"""
    response = client.get('/api/supported-types')
    assert response.status_code == 200
    data = response.get_json()
    assert 'supported_redaction_types' in data
    assert 'email' in data['supported_redaction_types']
    assert 'phone' in data['supported_redaction_types']


def test_redact_no_file(client):
    """Test redact endpoint without file"""
    response = client.post('/api/redact', data={
        'redaction_types': '["email", "phone"]'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_redact_invalid_file_type(client):
    """Test redact endpoint with invalid file type"""
    data = {
        'file': (io.BytesIO(b'test content'), 'test.txt'),
        'redaction_types': '["email", "phone"]'
    }
    response = client.post('/api/redact', data=data)
    assert response.status_code == 400
    result = response.get_json()
    assert 'error' in result


def test_preview_no_file(client):
    """Test preview endpoint without file"""
    response = client.post('/api/preview', data={
        'redaction_types': '["email"]'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
