# Gmail Setup - Quick Reference

## ⚡ 5-Minute Quick Start

**If you just want to get it working fast:**

### 1. Google Cloud Console (5 minutes)

```
1. Go to: https://console.cloud.google.com/
2. Create new project: "IGI Insurance"
3. Enable: Gmail API
4. OAuth consent screen: External → Fill required fields
5. Add scopes: gmail.readonly, gmail.modify
6. Add test user: your@gmail.com
7. Create credentials: OAuth 2.0 → Web application
8. Add redirect URI: http://localhost:8000/api/gmail/callback
9. Copy Client ID and Secret
```

### 2. Update .env (30 seconds)

```env
GMAIL_CLIENT_ID=your-actual-client-id-here
GMAIL_CLIENT_SECRET=your-actual-client-secret-here
GMAIL_REDIRECT_URI=http://localhost:8000/api/gmail/callback
```

### 3. Restart & Authenticate (2 minutes)

```bash
# Restart backend
docker compose restart backend

# Get auth URL
curl http://localhost:8000/api/gmail/auth-url

# Copy the auth_url from response
# Open in browser → Sign in → Allow permissions
```

### 4. Test (1 minute)

```bash
# Test authentication
curl http://localhost:8000/api/gmail/drafts

# Manual poll
curl -X POST http://localhost:8000/api/gmail/poll
```

---

## 📧 Test Email Format

Send yourself this email to test:

```
Subject: Car Insurance Request

Name: John Doe
Make: Toyota
Model: Corolla
Year: 2020
Engine: ABC123456
Chassis: XYZ789012
Sum Insured: PKR 2000000
```

Wait 5 minutes or trigger manual poll. Check: http://localhost:8000/api/gmail/drafts

---

## 🐛 Quick Fixes

**"No valid credentials"** → Complete step 3 (authentication)

**"Invalid client_id"** → Check you copied the FULL Client ID (very long)

**"Redirect URI mismatch"** → Must be exactly: `http://localhost:8000/api/gmail/callback`

**"Access blocked"** → Click "Go to IGI Insurance (unsafe)" - it's YOUR app

---

## 📚 Need Detailed Steps?

See **GMAIL_SETUP_GUIDE.md** for complete walkthrough with screenshots and troubleshooting.

---

**Done! Gmail automation now running every 5 minutes.** ✅
