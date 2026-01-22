# Deployment Guide - PDF Redaction Service

This guide will help you deploy your PDF redaction microservice to various cloud platforms and get a live API URL.

## 🚀 Quick Deploy Options

### Option 1: Render (Recommended - FREE)

**Pros:** Free tier, automatic deployments, easy setup
**Cons:** May sleep after inactivity (wakes up in ~30 seconds)

#### Steps:

1. **Push your code to GitHub** (already done!)

2. **Go to [Render.com](https://render.com)** and sign up

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `pdf-editor` repository
   - Choose the branch: `claude/pdf-redaction-service-frLNl`

4. **Configure Service**
   - Name: `pdf-redaction-service` (or your choice)
   - Region: Choose closest to you
   - Branch: `claude/pdf-redaction-service-frLNl`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app`

5. **Set Environment Variables**
   - Add `SECRET_KEY` → Generate a random string
   - Add `FLASK_ENV` → `production`

6. **Deploy!**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Your API URL will be: `https://your-service-name.onrender.com`

#### Test Your Deployment:
```bash
# Health check
curl https://your-service-name.onrender.com/health

# Get supported types
curl https://your-service-name.onrender.com/api/supported-types

# Redact PDF
curl -X POST https://your-service-name.onrender.com/api/redact \
  -F "file=@resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\"]" \
  -o redacted.pdf
```

---

### Option 2: Railway (FREE)

**Pros:** Free tier, great performance, GitHub integration
**Cons:** Credit card required (but won't charge on free tier)

#### Steps:

1. **Go to [Railway.app](https://railway.app)** and sign up

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `pdf-editor` repository
   - Select branch: `claude/pdf-redaction-service-frLNl`

3. **Railway Auto-Detects Configuration**
   - Railway will automatically detect the Dockerfile
   - No manual configuration needed!

4. **Set Environment Variables**
   - Go to "Variables" tab
   - Add `SECRET_KEY` → Generate random string
   - Add `FLASK_ENV` → `production`
   - Add `PORT` → `5000` (Railway provides this automatically)

5. **Generate Domain**
   - Go to "Settings" tab
   - Click "Generate Domain"
   - Your API URL will be: `https://your-app.up.railway.app`

6. **Deploy**
   - Railway automatically builds and deploys
   - Wait 2-3 minutes

#### Test:
```bash
curl https://your-app.up.railway.app/health
```

---

### Option 3: Fly.io (FREE)

**Pros:** Great performance, edge deployment, generous free tier
**Cons:** Requires CLI installation

#### Steps:

1. **Install Fly CLI**
   ```bash
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh

   # Windows
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Sign up for Fly.io**
   ```bash
   fly auth signup
   # or login if you have account
   fly auth login
   ```

3. **Navigate to your project**
   ```bash
   cd /path/to/pdf-editor
   ```

4. **Launch the app**
   ```bash
   fly launch
   ```

   When prompted:
   - App name: Choose a name (or press Enter for auto-generated)
   - Region: Choose closest to you
   - Would you like to set up a PostgreSQL database? **NO**
   - Would you like to deploy now? **YES**

5. **Set Environment Variables**
   ```bash
   fly secrets set SECRET_KEY="your-secret-key-here"
   fly secrets set FLASK_ENV="production"
   ```

6. **Deploy**
   ```bash
   fly deploy
   ```

7. **Get Your URL**
   ```bash
   fly status
   ```
   Your API URL will be: `https://your-app-name.fly.dev`

#### Test:
```bash
curl https://your-app-name.fly.dev/health
```

---

### Option 4: DigitalOcean App Platform

**Pros:** Reliable, good performance, simple pricing
**Cons:** Paid only (~$5/month minimum)

#### Steps:

1. **Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)**

2. **Create App**
   - Click "Create App"
   - Choose "GitHub" as source
   - Select your repository
   - Branch: `claude/pdf-redaction-service-frLNl`

3. **Configure**
   - DigitalOcean auto-detects Dockerfile
   - Set environment variables:
     - `SECRET_KEY`
     - `FLASK_ENV=production`

4. **Deploy**
   - Choose $5/month plan (Basic)
   - Click "Launch App"
   - Your URL: `https://your-app.ondigitalocean.app`

---

## 🔧 Configuration for Production

### Environment Variables (Set on your platform)

```bash
SECRET_KEY=your-super-secret-key-min-32-chars
FLASK_ENV=production
PORT=5000  # Usually auto-provided by platform
```

### Generate Secret Key
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📊 Free Tier Comparison

| Platform | Free Tier | Auto-Sleep | Build Time | Easy Setup |
|----------|-----------|------------|------------|------------|
| **Render** | ✅ Yes | After 15 min | 3-5 min | ⭐⭐⭐⭐⭐ |
| **Railway** | ✅ Yes ($5 credit) | No | 2-3 min | ⭐⭐⭐⭐⭐ |
| **Fly.io** | ✅ Yes | Optional | 3-4 min | ⭐⭐⭐⭐ |
| **Heroku** | ❌ Paid only | N/A | 2-3 min | ⭐⭐⭐⭐⭐ |
| **DigitalOcean** | ❌ $5/month | No | 3-5 min | ⭐⭐⭐⭐ |

**Recommendation:** Start with **Render** for completely free hosting or **Railway** for better performance.

---

## 🧪 Testing Your Deployed API

### 1. Health Check
```bash
curl https://your-api-url.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "pdf-redaction-service"
}
```

### 2. Get Supported Types
```bash
curl https://your-api-url.com/api/supported-types
```

### 3. Preview Redaction
```bash
curl -X POST https://your-api-url.com/api/preview \
  -F "file=@sample.pdf" \
  -F "redaction_types=[\"email\",\"phone\"]"
```

### 4. Redact PDF
```bash
curl -X POST https://your-api-url.com/api/redact \
  -F "file=@resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\",\"linkedin\"]" \
  -o redacted_output.pdf
```

---

## 🔗 Update Your MERN App

Once deployed, update your frontend to use the live API URL:

```javascript
// config.js or .env file
export const PDF_SERVICE_URL = 'https://your-api-url.com/api';

// In your React component
const response = await fetch(`${PDF_SERVICE_URL}/redact`, {
  method: 'POST',
  body: formData
});
```

### Node.js Backend
```javascript
const PDF_SERVICE_URL = process.env.PDF_SERVICE_URL || 'https://your-api-url.com/api';
```

---

## 🐛 Troubleshooting

### Build Fails with PyMuPDF
If deployment fails with PyMuPDF installation error:

**Solution:** The Dockerfile includes all necessary dependencies. Make sure your platform uses the Dockerfile for build.

For platforms using `requirements.txt` directly, you may need to use the Dockerfile build option in settings.

### App Crashes on Startup
Check logs:
```bash
# Render: View logs in dashboard
# Railway: railway logs
# Fly.io: fly logs
```

Common issues:
- Missing environment variables
- Port configuration (most platforms provide PORT automatically)
- Memory limits (increase if needed)

### CORS Errors
Update `app.py` to allow your frontend domain:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-frontend.com", "http://localhost:3000"]
    }
})
```

### Timeout Errors on Large PDFs
Increase worker timeout in start command:
```bash
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 300 app:app
```

---

## 📈 Monitoring

### Set Up Health Check Monitoring

Use UptimeRobot (free) to monitor your service:
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Add new monitor
3. URL: `https://your-api-url.com/health`
4. Get alerts if service goes down

### View Logs

**Render:**
```
Dashboard → Logs tab
```

**Railway:**
```bash
railway logs
```

**Fly.io:**
```bash
fly logs
```

---

## 🔐 Security for Production

### 1. Restrict CORS
Update `app.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-production-frontend.com"]
    }
})
```

### 2. Add Rate Limiting
```bash
pip install flask-limiter
```

Update `app.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

### 3. Use HTTPS Only
All the platforms above provide HTTPS by default.

### 4. Add Authentication (Optional)
For additional security, add API key authentication:
```python
from functools import wraps
from flask import request

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.environ.get('API_KEY'):
            return {'error': 'Invalid API key'}, 401
        return f(*args, **kwargs)
    return decorated_function

@api_bp.route('/redact', methods=['POST'])
@require_api_key
def redact_pdf():
    # ... existing code
```

---

## 🎯 Next Steps

1. **Deploy to Render** (easiest, free)
2. **Test your API** with the provided curl commands
3. **Update your MERN frontend** with the live API URL
4. **Set up monitoring** with UptimeRobot
5. **Configure CORS** for your production domain
6. **Add rate limiting** for production use

Your microservice is now production-ready! 🚀
