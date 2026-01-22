# New Features - Header, Footer & DOCX Support

## 🎉 New Capabilities

Your PDF Redaction Service now supports:

1. **Custom Headers with Logo** - Add company logo to document headers
2. **Custom Footers** - Add company contact information in footers
3. **Default Recrui8 Footer** - Pre-configured Recrui8 branding
4. **DOCX Output Format** - Download redacted documents as Word files
5. **Flexible Field Selection** - Choose exactly what to redact

---

## 📋 Acceptance Criteria - ✅ COMPLETED

- ✅ Contact number removed
- ✅ Contact email ID removed
- ✅ LinkedIn / Github contacts removed
- ✅ Recrui8 Logo added in Header
- ✅ "Recrui8.com | info@Recrui8.com | +91 922-6881-922" added in footer
- ✅ Option to choose fields to redact
- ✅ Option to download in DOCX & PDF format

---

## 🚀 API Usage

### Base URL
```
https://pdf-editor-4bfw.onrender.com/api
```

### New Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `redaction_types` | JSON array | Yes | Fields to redact: `["email", "phone", "linkedin", "portfolio"]` |
| `output_format` | String | No | Output format: `"pdf"` or `"docx"` (default: `"pdf"`) |
| `use_default_footer` | Boolean | No | Add Recrui8 footer (default: `false`) |
| `footer_text` | String | No | Custom footer text |
| `header_text` | String | No | Custom header text |
| `logo` | File | No | Logo image file (PNG/JPG) |

---

## 📝 Example Requests

### 1. Basic Redaction with Default Recrui8 Footer (PDF)

```bash
curl -X POST https://pdf-editor-4bfw.onrender.com/api/redact \
  -F "file=@resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\",\"linkedin\"]" \
  -F "use_default_footer=true" \
  -o redacted_resume.pdf
```

**What this does:**
- Removes email addresses
- Removes phone numbers
- Removes LinkedIn URLs
- Adds footer: "Recrui8.com | info@Recrui8.com | +91 922-6881-922"
- Downloads as PDF

---

### 2. Redaction with Logo and Default Footer (PDF)

```bash
curl -X POST https://pdf-editor-4bfw.onrender.com/api/redact \
  -F "file=@resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\",\"linkedin\",\"portfolio\"]" \
  -F "use_default_footer=true" \
  -F "logo=@recrui8_logo.png" \
  -o redacted_resume.pdf
```

**What this does:**
- Removes all contact information
- Adds Recrui8 logo in header
- Adds Recrui8 footer
- Downloads as PDF

---

### 3. Download as DOCX with Footer

```bash
curl -X POST https://pdf-editor-4bfw.onrender.com/api/redact \
  -F "file=@resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\"]" \
  -F "output_format=docx" \
  -F "use_default_footer=true" \
  -o redacted_resume.docx
```

**What this does:**
- Removes email and phone
- Adds Recrui8 footer
- **Downloads as DOCX** (Word format)

---

### 4. Custom Header and Footer

```bash
curl -X POST https://pdf-editor-4bfw.onrender.com/api/redact \
  -F "file=@resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\",\"linkedin\"]" \
  -F "header_text=Confidential Document" \
  -F "footer_text=Your Company | contact@company.com | +1-555-0000" \
  -F "output_format=pdf" \
  -o redacted_resume.pdf
```

**What this does:**
- Removes contact details
- Adds custom header text
- Adds custom footer with your branding
- Downloads as PDF

---

### 5. Full Options - Logo, Header, Footer, DOCX

```bash
curl -X POST https://pdf-editor-4bfw.onrender.com/api/redact \
  -F "file=@resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\",\"linkedin\",\"portfolio\"]" \
  -F "logo=@company_logo.png" \
  -F "header_text=Recruitment Department" \
  -F "footer_text=Recrui8.com | info@Recrui8.com | +91 922-6881-922" \
  -F "output_format=docx" \
  -o redacted_resume.docx
```

**What this does:**
- Removes ALL contact information
- Adds logo to header
- Adds custom header text
- Adds footer with Recrui8 branding
- **Downloads as DOCX**

---

## 💻 JavaScript Integration

### React Component Example

```javascript
import React, { useState } from 'react';

function ResumeRedactor() {
  const [pdfFile, setPdfFile] = useState(null);
  const [logoFile, setLogoFile] = useState(null);
  const [outputFormat, setOutputFormat] = useState('pdf');
  const [redactionOptions, setRedactionOptions] = useState({
    email: true,
    phone: true,
    linkedin: true,
    portfolio: false
  });
  const [useDefaultFooter, setUseDefaultFooter] = useState(true);

  const handleRedact = async () => {
    const formData = new FormData();

    // Add PDF file
    formData.append('file', pdfFile);

    // Add redaction types based on selected options
    const selectedTypes = Object.keys(redactionOptions).filter(
      key => redactionOptions[key]
    );
    formData.append('redaction_types', JSON.stringify(selectedTypes));

    // Add output format
    formData.append('output_format', outputFormat);

    // Add default footer flag
    formData.append('use_default_footer', useDefaultFooter.toString());

    // Add logo if provided
    if (logoFile) {
      formData.append('logo', logoFile);
    }

    try {
      const response = await fetch('https://pdf-editor-4bfw.onrender.com/api/redact', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Redaction failed');
      }

      // Download the file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `redacted_resume.${outputFormat}`;
      a.click();

      alert('Resume redacted successfully!');
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  return (
    <div className="resume-redactor">
      <h2>Redact Resume</h2>

      {/* File Upload */}
      <div>
        <label>Upload Resume (PDF):</label>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setPdfFile(e.target.files[0])}
        />
      </div>

      {/* Logo Upload */}
      <div>
        <label>Upload Logo (Optional):</label>
        <input
          type="file"
          accept=".png,.jpg,.jpeg"
          onChange={(e) => setLogoFile(e.target.files[0])}
        />
      </div>

      {/* Redaction Options */}
      <div>
        <h3>What to Redact:</h3>
        <label>
          <input
            type="checkbox"
            checked={redactionOptions.email}
            onChange={(e) => setRedactionOptions({
              ...redactionOptions,
              email: e.target.checked
            })}
          />
          Email Address
        </label>

        <label>
          <input
            type="checkbox"
            checked={redactionOptions.phone}
            onChange={(e) => setRedactionOptions({
              ...redactionOptions,
              phone: e.target.checked
            })}
          />
          Phone Number
        </label>

        <label>
          <input
            type="checkbox"
            checked={redactionOptions.linkedin}
            onChange={(e) => setRedactionOptions({
              ...redactionOptions,
              linkedin: e.target.checked
            })}
          />
          LinkedIn Profile
        </label>

        <label>
          <input
            type="checkbox"
            checked={redactionOptions.portfolio}
            onChange={(e) => setRedactionOptions({
              ...redactionOptions,
              portfolio: e.target.checked
            })}
          />
          Portfolio/GitHub Links
        </label>
      </div>

      {/* Output Format */}
      <div>
        <h3>Download Format:</h3>
        <label>
          <input
            type="radio"
            value="pdf"
            checked={outputFormat === 'pdf'}
            onChange={(e) => setOutputFormat(e.target.value)}
          />
          PDF
        </label>

        <label>
          <input
            type="radio"
            value="docx"
            checked={outputFormat === 'docx'}
            onChange={(e) => setOutputFormat(e.target.value)}
          />
          DOCX (Word)
        </label>
      </div>

      {/* Footer Options */}
      <div>
        <label>
          <input
            type="checkbox"
            checked={useDefaultFooter}
            onChange={(e) => setUseDefaultFooter(e.target.checked)}
          />
          Add Recrui8 Footer
        </label>
      </div>

      {/* Submit Button */}
      <button onClick={handleRedact} disabled={!pdfFile}>
        Redact & Download
      </button>
    </div>
  );
}

export default ResumeRedactor;
```

---

### Node.js/Express Backend Integration

```javascript
const express = require('express');
const multer = require('multer');
const FormData = require('form-data');
const fetch = require('node-fetch');
const fs = require('fs');

const app = express();
const upload = multer({ storage: multer.memoryStorage() });

const PDF_SERVICE_URL = 'https://pdf-editor-4bfw.onrender.com/api';

// Endpoint to redact resume for recruiter
app.post(
  '/api/recruiter/redact-resume',
  upload.fields([
    { name: 'resume', maxCount: 1 },
    { name: 'logo', maxCount: 1 }
  ]),
  async (req, res) => {
    try {
      const { redactionTypes, outputFormat, useDefaultFooter } = req.body;

      const formData = new FormData();

      // Add resume file
      formData.append('file', req.files.resume[0].buffer, {
        filename: req.files.resume[0].originalname,
        contentType: 'application/pdf'
      });

      // Add redaction types
      formData.append('redaction_types', redactionTypes || '["email","phone","linkedin"]');

      // Add output format
      formData.append('output_format', outputFormat || 'pdf');

      // Add default footer flag
      formData.append('use_default_footer', useDefaultFooter || 'true');

      // Add logo if provided
      if (req.files.logo && req.files.logo[0]) {
        formData.append('logo', req.files.logo[0].buffer, {
          filename: req.files.logo[0].originalname,
          contentType: req.files.logo[0].mimetype
        });
      }

      // Call PDF redaction service
      const response = await fetch(`${PDF_SERVICE_URL}/redact`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('PDF redaction service failed');
      }

      // Get the redacted file
      const redactedFile = await response.buffer();

      // Set response headers
      const fileExtension = outputFormat || 'pdf';
      const mimeType = fileExtension === 'docx'
        ? 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        : 'application/pdf';

      res.set('Content-Type', mimeType);
      res.set('Content-Disposition', `attachment; filename=redacted_resume.${fileExtension}`);
      res.send(redactedFile);

    } catch (error) {
      console.error('Error:', error);
      res.status(500).json({ error: error.message });
    }
  }
);

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

---

## 🎯 Common Use Cases

### Use Case 1: Recruiter Reviews Resume (Remove All Contact Info)

```bash
curl -X POST https://pdf-editor-4bfw.onrender.com/api/redact \
  -F "file=@candidate_resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\",\"linkedin\",\"portfolio\"]" \
  -F "use_default_footer=true" \
  -F "logo=@recrui8_logo.png" \
  -o candidate_resume_redacted.pdf
```

### Use Case 2: Share Resume Externally (DOCX Format)

```bash
curl -X POST https://pdf-editor-4bfw.onrender.com/api/redact \
  -F "file=@resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\"]" \
  -F "output_format=docx" \
  -F "use_default_footer=true" \
  -o resume_for_client.docx
```

### Use Case 3: Preview What Will Be Redacted

```bash
curl -X POST https://pdf-editor-4bfw.onrender.com/api/preview \
  -F "file=@resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\",\"linkedin\"]"
```

**Response:**
```json
{
  "success": true,
  "sensitive_data": {
    "emails": ["candidate@email.com"],
    "phones": ["+1-555-123-4567", "(555) 987-6543"],
    "linkedin": ["https://linkedin.com/in/candidate"],
    "portfolios": [],
    "urls": []
  },
  "metadata": {
    "page_count": 2
  }
}
```

---

## 🔧 Supported Redaction Types

| Type | Description | Example |
|------|-------------|---------|
| `email` | Email addresses | `john@example.com` |
| `phone` | Phone numbers (all formats) | `(555) 123-4567`, `+1-555-123-4567` |
| `linkedin` | LinkedIn profile URLs | `https://linkedin.com/in/johndoe` |
| `portfolio` | Portfolio/GitHub URLs | `https://github.com/johndoe` |
| `all_urls` | All URLs | Any web address |

---

## 📦 Supported Output Formats

| Format | MIME Type | Extension | Use Case |
|--------|-----------|-----------|----------|
| PDF | `application/pdf` | `.pdf` | Final documents, archiving |
| DOCX | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | `.docx` | Further editing, Word users |

---

## ✅ Testing Checklist

- [ ] Test PDF redaction with default footer
- [ ] Test DOCX output
- [ ] Test with logo upload
- [ ] Test custom header text
- [ ] Test custom footer text
- [ ] Test selecting different redaction types
- [ ] Test preview mode
- [ ] Integrate with your MERN app

---

## 🚀 Next Steps

1. **Test the new features:**
   ```bash
   # Download a sample resume PDF and test
   curl -X POST https://pdf-editor-4bfw.onrender.com/api/redact \
     -F "file=@test_resume.pdf" \
     -F "redaction_types=[\"email\",\"phone\"]" \
     -F "use_default_footer=true" \
     -F "output_format=pdf" \
     -o result.pdf
   ```

2. **Create your logo:**
   - Create a PNG or JPG logo (recommended size: 200x60 pixels)
   - Save as `recrui8_logo.png`

3. **Integrate with your frontend:**
   - Use the React component example above
   - Customize the UI to match your design

4. **Deploy updates:**
   - The service is already live and updated
   - Start using the new features immediately!

---

## 📞 Support

- **API URL:** https://pdf-editor-4bfw.onrender.com
- **Health Check:** https://pdf-editor-4bfw.onrender.com/health
- **Supported Types:** https://pdf-editor-4bfw.onrender.com/api/supported-types

All new features are live and ready to use! 🎉
