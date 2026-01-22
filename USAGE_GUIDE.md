# PDF Redaction Service - Usage Guide

## Quick Start

### 1. Start the Service

**Option A: Using Python directly**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Option B: Using Docker**
```bash
docker build -t pdf-redaction-service .
docker run -p 5000:5000 pdf-redaction-service
```

**Option C: Using Docker Compose**
```bash
docker-compose up -d
```

### 2. Test the Service

```bash
# Check if service is running
curl http://localhost:5000/health

# Get supported redaction types
curl http://localhost:5000/api/supported-types
```

### 3. Redact a PDF

```bash
curl -X POST http://localhost:5000/api/redact \
  -F "file=@your_resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\",\"linkedin\"]" \
  -o redacted_resume.pdf
```

## Use Cases

### Use Case 1: Recruiter Reviewing Resumes

**Scenario:** A recruiter wants to review resumes without seeing contact information to reduce bias.

**Solution:**
```javascript
// In your React recruitment app
const redactResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('redaction_types', JSON.stringify(['email', 'phone', 'linkedin', 'portfolio']));

  const response = await fetch('http://localhost:5000/api/redact', {
    method: 'POST',
    body: formData
  });

  const blob = await response.blob();
  return blob; // Display or download the redacted PDF
};
```

### Use Case 2: Preview Before Redacting

**Scenario:** See what information will be redacted before committing.

**Solution:**
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
    "emails": ["john.doe@email.com"],
    "phones": ["(555) 123-4567"],
    "linkedin": [],
    "portfolios": [],
    "urls": []
  },
  "metadata": {
    "page_count": 2
  }
}
```

### Use Case 3: Batch Processing

**Scenario:** Redact multiple resumes at once.

**Solution:**
```bash
curl -X POST http://localhost:5000/api/batch-redact \
  -F "files=@resume1.pdf" \
  -F "files=@resume2.pdf" \
  -F "files=@resume3.pdf" \
  -F "redaction_types=[\"email\",\"phone\"]"
```

## Integration with MERN Stack

### Backend (Node.js/Express)

```javascript
// routes/recruiter.js
const express = require('express');
const multer = require('multer');
const FormData = require('form-data');
const fetch = require('node-fetch');

const router = express.Router();
const upload = multer({ storage: multer.memoryStorage() });

const PDF_SERVICE = 'http://localhost:5000/api';

router.post('/applications/:id/redact', upload.single('resume'), async (req, res) => {
  try {
    const { redactionTypes } = req.body;

    // Forward to PDF redaction service
    const formData = new FormData();
    formData.append('file', req.file.buffer, {
      filename: req.file.originalname,
      contentType: 'application/pdf'
    });
    formData.append('redaction_types', redactionTypes);

    const response = await fetch(`${PDF_SERVICE}/redact`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error('Redaction failed');
    }

    const redactedPDF = await response.buffer();

    // Save to your database or cloud storage
    // ... your storage logic ...

    res.json({
      success: true,
      message: 'Resume redacted successfully'
    });

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
```

### Frontend (React)

```javascript
// components/ResumeRedactor.jsx
import React, { useState } from 'react';
import axios from 'axios';

function ResumeRedactor({ applicationId, resumeFile }) {
  const [redacting, setRedacting] = useState(false);
  const [redactionTypes, setRedactionTypes] = useState({
    email: true,
    phone: true,
    linkedin: true,
    portfolio: true
  });

  const handleRedact = async () => {
    setRedacting(true);

    try {
      const formData = new FormData();
      formData.append('resume', resumeFile);
      formData.append('redactionTypes', JSON.stringify(
        Object.keys(redactionTypes).filter(key => redactionTypes[key])
      ));

      const response = await axios.post(
        `/api/applications/${applicationId}/redact`,
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      );

      alert('Resume redacted successfully!');

    } catch (error) {
      alert('Failed to redact resume: ' + error.message);
    } finally {
      setRedacting(false);
    }
  };

  return (
    <div className="resume-redactor">
      <h3>Redact Resume</h3>

      <div className="redaction-options">
        <label>
          <input
            type="checkbox"
            checked={redactionTypes.email}
            onChange={(e) => setRedactionTypes({
              ...redactionTypes,
              email: e.target.checked
            })}
          />
          Hide Email
        </label>

        <label>
          <input
            type="checkbox"
            checked={redactionTypes.phone}
            onChange={(e) => setRedactionTypes({
              ...redactionTypes,
              phone: e.target.checked
            })}
          />
          Hide Phone
        </label>

        <label>
          <input
            type="checkbox"
            checked={redactionTypes.linkedin}
            onChange={(e) => setRedactionTypes({
              ...redactionTypes,
              linkedin: e.target.checked
            })}
          />
          Hide LinkedIn
        </label>

        <label>
          <input
            type="checkbox"
            checked={redactionTypes.portfolio}
            onChange={(e) => setRedactionTypes({
              ...redactionTypes,
              portfolio: e.target.checked
            })}
          />
          Hide Portfolio
        </label>
      </div>

      <button
        onClick={handleRedact}
        disabled={redacting}
      >
        {redacting ? 'Redacting...' : 'Redact Resume'}
      </button>
    </div>
  );
}

export default ResumeRedactor;
```

## Advanced Configuration

### Custom Redaction Patterns

To add custom patterns, edit `app/services/redaction_patterns.py`:

```python
# Add a custom pattern for SSN
SSN_PATTERN = re.compile(
    r'\b\d{3}-\d{2}-\d{4}\b',
    re.IGNORECASE
)

@classmethod
def find_ssn(cls, text):
    """Find Social Security Numbers"""
    return cls.SSN_PATTERN.findall(text)
```

### Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-production-secret-key
FLASK_ENV=production
MAX_CONTENT_LENGTH=16777216
```

### CORS Configuration

To restrict CORS to specific origins, edit `app.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://your-recruitment-site.com",
            "http://localhost:3000"
        ]
    }
})
```

## Monitoring and Logging

### Enable Logging

Add to `config.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('redaction_service.log'),
        logging.StreamHandler()
    ]
)
```

### Health Check

The `/health` endpoint can be used with monitoring tools:

```bash
# Add to your monitoring script
curl -f http://localhost:5000/health || alert_team
```

## Troubleshooting

### Issue: Service won't start

**Solution:**
```bash
# Check if port 5000 is already in use
lsof -i :5000

# Kill the process or use a different port
docker run -p 5001:5000 pdf-redaction-service
```

### Issue: PyMuPDF installation fails

**Solution:**
```bash
# Install system dependencies first
sudo apt-get update
sudo apt-get install -y gcc g++ libfreetype6-dev libjpeg-dev

# Then install Python packages
pip install -r requirements.txt
```

### Issue: Large PDF files fail

**Solution:** Increase the max content length in `config.py`:

```python
MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB
```

## Performance Optimization

### For High-Volume Processing

1. **Use Multiple Workers:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Scale with Docker:**
```yaml
# docker-compose.yml
services:
  pdf-redaction:
    deploy:
      replicas: 3
```

3. **Add Caching:** Implement Redis caching for frequently processed PDFs.

## Security Best Practices

1. **Use HTTPS in production**
2. **Implement rate limiting**
3. **Add authentication/authorization**
4. **Sanitize file inputs**
5. **Set up proper CORS policies**
6. **Regular security updates**

```bash
# Update dependencies regularly
pip list --outdated
pip install --upgrade -r requirements.txt
```
