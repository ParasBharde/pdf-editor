# PDF Redaction Microservice

A powerful Python microservice for automatically redacting sensitive information from PDF documents. Built with Flask and PyMuPDF, designed for seamless integration with MERN stack applications.

## 🚀 Features

- **Automatic Detection & Redaction** of:
  - Email addresses
  - Phone numbers (multiple formats)
  - LinkedIn profile URLs
  - Portfolio/GitHub URLs
  - All URLs (optional)

- **Flexible API** with:
  - Single PDF redaction
  - Batch processing
  - Preview mode (detect without redacting)
  - Multiple output formats

- **Production-Ready**:
  - Docker support
  - CORS enabled for frontend integration
  - Comprehensive error handling
  - File validation

## 📋 Prerequisites

- Python 3.11+
- pip
- Docker (optional)

## 🛠️ Installation

### Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd pdf-editor
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

5. Run the service:
```bash
python app.py
```

The service will be available at `http://localhost:5000`

### Docker Setup

1. Build the Docker image:
```bash
docker build -t pdf-redaction-service .
```

2. Run the container:
```bash
docker run -p 5000:5000 pdf-redaction-service
```

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "pdf-redaction-service"
}
```

---

#### 2. Get Supported Types
```http
GET /api/supported-types
```

**Response:**
```json
{
  "supported_redaction_types": {
    "email": "Email addresses",
    "phone": "Phone numbers",
    "linkedin": "LinkedIn profile URLs",
    "portfolio": "Portfolio/GitHub URLs",
    "all_urls": "All URLs"
  },
  "supported_output_formats": ["pdf"]
}
```

---

#### 3. Redact PDF
```http
POST /api/redact
```

**Parameters:**
- `file` (required): PDF file
- `redaction_types` (required): JSON array of types to redact
- `output_format` (optional): Output format (default: "pdf")
- `preview` (optional): Boolean, preview mode (default: false)

**Example Request (cURL):**
```bash
curl -X POST http://localhost:5000/api/redact \
  -F "file=@resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\",\"linkedin\"]" \
  -F "output_format=pdf"
```

**Example Request (JavaScript/Fetch):**
```javascript
const formData = new FormData();
formData.append('file', pdfFile);
formData.append('redaction_types', JSON.stringify(['email', 'phone', 'linkedin']));
formData.append('output_format', 'pdf');

const response = await fetch('http://localhost:5000/api/redact', {
  method: 'POST',
  body: formData
});

const blob = await response.blob();
// Download or display the redacted PDF
```

**Response:**
Returns the redacted PDF file for download.

---

#### 4. Preview Redaction
```http
POST /api/preview
```

**Parameters:**
- `file` (required): PDF file
- `redaction_types` (required): JSON array of types to redact

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/preview \
  -F "file=@resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\"]"
```

**Response:**
```json
{
  "success": true,
  "sensitive_data": {
    "emails": ["john@example.com"],
    "phones": ["123-456-7890", "+1 (555) 123-4567"],
    "linkedin": ["https://linkedin.com/in/johndoe"],
    "portfolios": ["https://github.com/johndoe"],
    "urls": []
  },
  "metadata": {
    "page_count": 2,
    "is_encrypted": false
  },
  "redaction_types": ["email", "phone"],
  "message": "Preview of data that will be redacted"
}
```

---

#### 5. Batch Redact
```http
POST /api/batch-redact
```

**Parameters:**
- `files` (required): Multiple PDF files
- `redaction_types` (required): JSON array of types to redact
- `output_format` (optional): Output format (default: "pdf")

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/batch-redact \
  -F "files=@resume1.pdf" \
  -F "files=@resume2.pdf" \
  -F "redaction_types=[\"email\",\"phone\"]"
```

**Response:**
```json
{
  "success": true,
  "processed": 2,
  "errors": 0,
  "results": [
    {
      "filename": "resume1.pdf",
      "redacted_count": {
        "emails": 1,
        "phones": 2
      },
      "success": true
    }
  ],
  "error_details": []
}
```

## 🔗 Integration Examples

### React/MERN Frontend Integration

```javascript
// PDFRedactionService.js
export class PDFRedactionService {
  constructor(baseUrl = 'http://localhost:5000/api') {
    this.baseUrl = baseUrl;
  }

  async redactPDF(file, redactionTypes, preview = false) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('redaction_types', JSON.stringify(redactionTypes));
    if (preview) {
      formData.append('preview', 'true');
    }

    const endpoint = preview ? '/preview' : '/redact';
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to process PDF');
    }

    if (preview) {
      return await response.json();
    }

    return await response.blob();
  }

  async getSupportedTypes() {
    const response = await fetch(`${this.baseUrl}/supported-types`);
    return await response.json();
  }
}

// Usage in React Component
import React, { useState } from 'react';
import { PDFRedactionService } from './PDFRedactionService';

function PDFRedactor() {
  const [file, setFile] = useState(null);
  const [redactionTypes, setRedactionTypes] = useState(['email', 'phone']);
  const [preview, setPreview] = useState(null);

  const service = new PDFRedactionService();

  const handlePreview = async () => {
    if (!file) return;

    const result = await service.redactPDF(file, redactionTypes, true);
    setPreview(result.sensitive_data);
  };

  const handleRedact = async () => {
    if (!file) return;

    const blob = await service.redactPDF(file, redactionTypes, false);

    // Download the redacted PDF
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'redacted.pdf';
    a.click();
  };

  return (
    <div>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <div>
        <label>
          <input
            type="checkbox"
            checked={redactionTypes.includes('email')}
            onChange={(e) => {
              if (e.target.checked) {
                setRedactionTypes([...redactionTypes, 'email']);
              } else {
                setRedactionTypes(redactionTypes.filter(t => t !== 'email'));
              }
            }}
          />
          Email
        </label>

        <label>
          <input
            type="checkbox"
            checked={redactionTypes.includes('phone')}
            onChange={(e) => {
              if (e.target.checked) {
                setRedactionTypes([...redactionTypes, 'phone']);
              } else {
                setRedactionTypes(redactionTypes.filter(t => t !== 'phone'));
              }
            }}
          />
          Phone
        </label>

        {/* Add more checkboxes for other types */}
      </div>

      <button onClick={handlePreview}>Preview</button>
      <button onClick={handleRedact}>Redact & Download</button>

      {preview && (
        <div>
          <h3>Found Sensitive Data:</h3>
          <pre>{JSON.stringify(preview, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default PDFRedactor;
```

### Node.js/Express Backend Integration

```javascript
const express = require('express');
const multer = require('multer');
const FormData = require('form-data');
const fetch = require('node-fetch');

const app = express();
const upload = multer({ storage: multer.memoryStorage() });

const PDF_SERVICE_URL = 'http://localhost:5000/api';

app.post('/recruiter/redact-resume', upload.single('resume'), async (req, res) => {
  try {
    const { redactionTypes } = req.body;

    const formData = new FormData();
    formData.append('file', req.file.buffer, {
      filename: req.file.originalname,
      contentType: 'application/pdf'
    });
    formData.append('redaction_types', redactionTypes);

    const response = await fetch(`${PDF_SERVICE_URL}/redact`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error('PDF redaction failed');
    }

    const redactedPDF = await response.buffer();

    res.set('Content-Type', 'application/pdf');
    res.set('Content-Disposition', 'attachment; filename=redacted_resume.pdf');
    res.send(redactedPDF);

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000);
```

## 🏗️ Architecture

```
pdf-editor/
├── app/
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── services/
│   │   ├── pdf_processor.py   # PDF processing logic
│   │   └── redaction_patterns.py  # Detection patterns
│   └── utils/
│       └── validators.py      # Input validation
├── app.py                     # Application entry point
├── config.py                  # Configuration
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
└── README.md
```

## 🔒 Security Considerations

- File size limited to 16MB by default (configurable)
- Only PDF files are accepted
- Temporary files are cleaned up after processing
- CORS can be configured for specific origins
- Input validation on all endpoints

## 🧪 Testing

Run tests:
```bash
pytest
```

## 🚀 Deployment

### Production Deployment (Docker)

1. Set production environment variables:
```bash
export SECRET_KEY="your-production-secret-key"
export FLASK_ENV="production"
```

2. Build and run:
```bash
docker build -t pdf-redaction-service:prod .
docker run -d -p 5000:5000 \
  -e SECRET_KEY="your-secret-key" \
  -e FLASK_ENV="production" \
  --name pdf-redaction \
  pdf-redaction-service:prod
```

### Deploy with Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  pdf-redaction:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_ENV=production
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

## 📊 Performance

- Processes typical resume PDF (1-2 pages) in < 1 second
- Supports batch processing of multiple PDFs
- Memory efficient with streaming
- Scales horizontally with multiple containers

## 🐛 Troubleshooting

### PyMuPDF installation issues
If you encounter issues installing PyMuPDF, ensure you have the required system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get install gcc g++ libfreetype6-dev libjpeg-dev

# macOS
brew install freetype jpeg
```

### CORS issues
Update CORS configuration in `app.py`:
```python
CORS(app, resources={r"/api/*": {"origins": "https://your-frontend-domain.com"}})
```

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.