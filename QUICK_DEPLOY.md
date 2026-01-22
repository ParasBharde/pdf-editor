# 🚀 Quick Deployment Guide

Get your PDF Redaction API live in **5 minutes**!

## Fastest Way to Deploy (Render - 100% FREE)

### Step 1: Prepare
```bash
# Generate a secret key
python3 scripts/generate_secret.py
# Copy the output - you'll need it in Step 4
```

### Step 2: Deploy to Render
1. Go to **[render.com](https://render.com)** and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your **GitHub** account
4. Select repository: **`pdf-editor`**
5. Select branch: **`claude/pdf-redaction-service-frLNl`**

### Step 3: Configure
```
Name: pdf-redaction-service (or your choice)
Region: Choose closest to you
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app
```

### Step 4: Set Environment Variables
Click "Advanced" → Add Environment Variables:
```
SECRET_KEY = [paste the secret key from Step 1]
FLASK_ENV = production
```

### Step 5: Deploy!
Click **"Create Web Service"**

Wait 3-5 minutes... ☕

### Step 6: Get Your API URL
Your API will be live at:
```
https://your-service-name.onrender.com
```

### Step 7: Test It
```bash
# Test health
curl https://your-service-name.onrender.com/health

# Or use our test script
./scripts/test_deployed_api.sh https://your-service-name.onrender.com
```

---

## Use Your API

### From React/Frontend:
```javascript
const API_URL = 'https://your-service-name.onrender.com/api';

const formData = new FormData();
formData.append('file', pdfFile);
formData.append('redaction_types', JSON.stringify(['email', 'phone', 'linkedin']));

const response = await fetch(`${API_URL}/redact`, {
  method: 'POST',
  body: formData
});

const blob = await response.blob();
```

### From Node.js Backend:
```javascript
const PDF_API = 'https://your-service-name.onrender.com/api';

const formData = new FormData();
formData.append('file', req.file.buffer, {
  filename: req.file.originalname,
  contentType: 'application/pdf'
});
formData.append('redaction_types', JSON.stringify(['email', 'phone']));

const response = await fetch(`${PDF_API}/redact`, {
  method: 'POST',
  body: formData
});
```

### From cURL:
```bash
curl -X POST https://your-service-name.onrender.com/api/redact \
  -F "file=@resume.pdf" \
  -F "redaction_types=[\"email\",\"phone\",\"linkedin\"]" \
  -o redacted.pdf
```

---

## Alternative Platforms

### Railway (Also Free)
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repo and branch
4. Add environment variables (same as above)
5. Generate domain
6. Done! 🎉

### Fly.io (Free with CLI)
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
fly launch
# Follow prompts, choose free tier

# Set secrets
fly secrets set SECRET_KEY="your-secret-key"
fly secrets set FLASK_ENV="production"

# Deploy
fly deploy

# Get URL
fly status
```

---

## Important Notes

### Free Tier Limitations
- **Render Free**: Service sleeps after 15 min of inactivity (wakes in ~30 sec on first request)
- **Railway**: $5 free credit per month (usually enough for testing)
- **Fly.io**: 3 free VMs with 256MB RAM each

### For Production Use
Consider upgrading to paid tier (~$7-10/month) for:
- No sleep/always-on service
- Better performance
- More memory
- Custom domain support

---

## Need Help?

### Check Deployment Status
**Render**: View logs in dashboard
**Railway**: `railway logs`
**Fly.io**: `fly logs`

### Common Issues

**Build fails?**
- Make sure branch is correct: `claude/pdf-redaction-service-frLNl`
- Check build logs for errors

**App crashes?**
- Verify environment variables are set
- Check logs for error messages

**Can't connect?**
- Wait 3-5 minutes after deployment
- Check if service is awake (Render free tier sleeps)

**CORS errors?**
- Update `app.py` with your frontend URL
- Redeploy after changes

---

## Full Documentation

For detailed deployment instructions and other platforms:
📖 See [DEPLOYMENT.md](DEPLOYMENT.md)

For API usage and integration:
📖 See [README.md](README.md)

For usage examples:
📖 See [USAGE_GUIDE.md](USAGE_GUIDE.md)

---

## 🎉 You're Done!

Your PDF redaction microservice is now live and ready to integrate with your MERN recruiting platform!

Share your API URL with your team and start redacting PDFs! 🚀
