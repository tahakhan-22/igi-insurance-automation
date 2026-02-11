# Gmail OAuth 2.0 Setup Guide

## 🎯 What You'll Set Up

This guide will help you set up Gmail integration so the system can:
- Read unread emails from your Gmail inbox
- Automatically detect car insurance inquiries
- Extract client and vehicle data from emails
- Create draft policies automatically

**Security:** Uses OAuth 2.0 (Google's secure authentication) - **NO passwords stored!**

---

## ⏱️ Time Required

**~15 minutes** (one-time setup)

---

## 📋 Prerequisites

Before starting, make sure you have:

1. ✅ A Gmail account (any Gmail account)
2. ✅ Access to Google Cloud Console (free)
3. ✅ The IGI Insurance system running (`docker compose up`)

---

## 🚀 Step-by-Step Setup

### Step 1: Go to Google Cloud Console

1. Open your browser
2. Go to: https://console.cloud.google.com/
3. Sign in with your Gmail account

---

### Step 2: Create a New Project

1. Click the **project dropdown** at the top (says "Select a project")
2. Click **"NEW PROJECT"** button (top right)
3. Fill in:
   - **Project name:** `IGI Insurance Automation` (or any name)
   - **Organization:** Leave as "No organization"
4. Click **"CREATE"**
5. Wait ~30 seconds for project creation
6. **Select your new project** from the dropdown

---

### Step 3: Enable Gmail API

1. In the left sidebar, click **"APIs & Services"** → **"Library"**
2. In the search box, type: `Gmail API`
3. Click on **"Gmail API"** from results
4. Click the blue **"ENABLE"** button
5. Wait for it to enable (~10 seconds)

---

### Step 4: Configure OAuth Consent Screen

1. In left sidebar, click **"APIs & Services"** → **"OAuth consent screen"**
2. Select **"External"** (allows any Gmail user)
3. Click **"CREATE"**

**Fill in the form:**

**App Information:**
- **App name:** `IGI Insurance System`
- **User support email:** Select your email from dropdown
- **App logo:** (optional, skip for now)

**App Domain:**
- **Application home page:** `http://localhost:8000` (or your domain)
- **Privacy policy:** (optional, skip for now)
- **Terms of service:** (optional, skip for now)

**Developer Contact:**
- **Email addresses:** Your email (e.g., `your-email@gmail.com`)

4. Click **"SAVE AND CONTINUE"**

**Scopes (Step 2):**
5. Click **"ADD OR REMOVE SCOPES"**
6. In the filter box, type: `gmail`
7. Check these two scopes:
   - ✅ `.../auth/gmail.readonly` - Read emails
   - ✅ `.../auth/gmail.modify` - Mark as read
8. Click **"UPDATE"** button at bottom
9. Click **"SAVE AND CONTINUE"**

**Test Users (Step 3):**
10. Click **"ADD USERS"**
11. Enter the Gmail address you'll use for testing
12. Click **"ADD"**
13. Click **"SAVE AND CONTINUE"**

**Summary (Step 4):**
14. Review and click **"BACK TO DASHBOARD"**

---

### Step 5: Create OAuth 2.0 Credentials

1. In left sidebar, click **"APIs & Services"** → **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** at top
3. Select **"OAuth client ID"**

**Configure:**
- **Application type:** Select **"Web application"**
- **Name:** `IGI Insurance Web Client`

**Authorized redirect URIs:**
4. Click **"+ ADD URI"**
5. Enter: `http://localhost:8000/api/gmail/callback`
6. If you have a production domain, add it too: `https://yourdomain.com/api/gmail/callback`

7. Click **"CREATE"**

**Important - Copy Your Credentials:**

You'll see a popup with:
- ✅ **Client ID** (looks like: `123456789-abc...xyz.apps.googleusercontent.com`)
- ✅ **Client Secret** (looks like: `GOCSPX-abc...xyz`)

📝 **COPY THESE NOW!** You'll need them in the next step.

You can also download the JSON file, but you only need the two values above.

---

### Step 6: Update Your .env File

1. Open your `.env` file in the project root
2. Find these lines:

```env
GMAIL_CLIENT_ID=your-google-client-id
GMAIL_CLIENT_SECRET=your-google-client-secret
GMAIL_REDIRECT_URI=http://localhost:8000/api/gmail/callback
```

3. Replace with your actual values:

```env
GMAIL_CLIENT_ID=123456789-abc...xyz.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-abc...xyz
GMAIL_REDIRECT_URI=http://localhost:8000/api/gmail/callback
```

4. **Save the file**

---

### Step 7: Restart the Backend

If your system is already running:

```bash
# Stop the system
Ctrl+C

# Restart with new .env values
docker compose up --build
```

Or just restart the backend container:

```bash
docker compose restart backend
```

---

### Step 8: First-Time Authentication

Now you need to authenticate once so the system can access your Gmail.

**Option A: Using Browser (Easiest)**

1. Open your browser
2. Go to: http://localhost:8000/api/gmail/auth-url
3. You'll see a JSON response with an `auth_url`
4. Copy that URL and paste it in your browser
5. You'll see Google's login/consent screen:
   - Sign in with your Gmail account
   - Click **"Continue"** on the warning (it's your app)
   - Review permissions (read emails, modify emails)
   - Click **"Allow"**
6. You'll be redirected to: `http://localhost:8000/api/gmail/callback?code=...`
7. You should see: `{"message": "Gmail authentication successful"}`

**Option B: Using API Docs**

1. Go to: http://localhost:8000/docs
2. Find the **"Gmail Integration"** section
3. Click on `GET /api/gmail/auth-url`
4. Click **"Try it out"** → **"Execute"**
5. Copy the `auth_url` from the response
6. Follow steps 4-7 from Option A above

---

### Step 9: Test Gmail Integration

**Test 1: Check Authentication**

```bash
curl http://localhost:8000/api/gmail/drafts
```

You should see a list of draft policies (empty at first).

**Test 2: Manual Poll**

```bash
curl -X POST http://localhost:8000/api/gmail/poll
```

This will check your Gmail inbox for car insurance emails.

**Test 3: Send a Test Email**

1. Send an email to your Gmail account with subject: `Car Insurance Inquiry`
2. In the body, include:
   ```
   Name: John Doe
   Make: Toyota
   Model: Corolla
   Year: 2020
   Engine: ABC123456
   Chassis: XYZ789012
   Sum Insured: PKR 2000000
   ```
3. Wait ~5 minutes (or trigger manual poll)
4. Check: http://localhost:8000/api/gmail/drafts
5. You should see a new draft policy created!

---

## ✅ Verification Checklist

Make sure everything works:

- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth consent screen configured
- [ ] OAuth credentials created
- [ ] Client ID and Secret in .env file
- [ ] Backend restarted with new config
- [ ] First-time authentication completed
- [ ] Test poll returns success
- [ ] Draft policies API accessible

---

## 🔄 How It Works (After Setup)

Once set up, the system automatically:

1. **Every 5 minutes:** Checks Gmail inbox for unread emails
2. **Classify:** Looks for car insurance keywords
3. **Extract:** Uses regex to pull out client/vehicle data
4. **Create:** Makes a draft policy in the database
5. **Mark Read:** So it's not processed again

**You can monitor it:**
- Logs: `docker compose logs backend | grep gmail`
- API: `http://localhost:8000/api/gmail/drafts`

---

## 🔐 Security Best Practices

1. **Never commit credentials:** The `.env` file is already in `.gitignore`
2. **Use separate Gmail account:** Consider creating `igi-automation@yourdomain.com`
3. **Restrict scopes:** We only use `readonly` and `modify` (not full access)
4. **Monitor usage:** Check Google Cloud Console → APIs & Services → Dashboard
5. **Revoke if needed:** You can revoke access anytime at: https://myaccount.google.com/permissions

---

## 🐛 Troubleshooting

### Error: "No valid credentials. Please authenticate first."

**Solution:** Complete Step 8 (First-Time Authentication)

### Error: "Invalid client_id"

**Solution:** Check that you copied the full Client ID to `.env` (it's very long)

### Error: "Redirect URI mismatch"

**Solution:** 
1. In Google Cloud Console, verify redirect URI is: `http://localhost:8000/api/gmail/callback`
2. Check that .env has the same URI
3. Make sure no typos (especially http vs https)

### Error: "Access blocked: IGI Insurance System has not completed verification"

**Solution:**
1. This happens with "External" app type
2. Click "Go to IGI Insurance System (unsafe)" - it's YOUR app
3. Or add your email as a test user in OAuth consent screen

### Gmail polling not creating policies

**Check:**
1. Does email contain car insurance keywords? (car insurance, motor insurance, vehicle)
2. Is email unread?
3. Check backend logs: `docker compose logs backend | grep -i gmail`
4. Try manual poll: `POST http://localhost:8000/api/gmail/poll`

### Authentication expired

**Solution:**
The token auto-refreshes, but if it fails:
1. Delete `/tmp/gmail_token.pickle` (inside backend container)
2. Re-authenticate (Step 8)

---

## 📚 Related Documentation

- **PROJECT_OVERVIEW.md** - How Gmail automation works
- **GETTING_STARTED.md** - Initial system setup
- **TROUBLESHOOTING.md** - General troubleshooting
- **API Docs** - http://localhost:8000/docs

---

## 🎉 You're Done!

Gmail integration is now set up and running!

The system will automatically:
- ✅ Poll Gmail every 5 minutes
- ✅ Detect car insurance emails
- ✅ Extract client and vehicle data
- ✅ Create draft policies
- ✅ Mark emails as read

**Next Steps:**
1. Test with real emails
2. Monitor draft policies: http://localhost:8000/api/gmail/drafts
3. Review and approve drafts
4. Convert to full policies

---

## 💡 Tips

**For Testing:**
- Use keywords: "car insurance", "motor insurance", "vehicle policy"
- Include vehicle details: make, model, year, engine, chassis
- The more structured your email, the better the extraction

**For Production:**
- Set up a dedicated email: `igi-insurance@yourdomain.com`
- Create email templates for clients/agents
- Monitor daily: `GET /api/gmail/drafts`
- Archive processed drafts regularly

**Email Template Example:**
```
Subject: New Motor Insurance Request

Client Name: Jane Smith
Phone: +923001234567
Email: jane.smith@example.com

Vehicle Details:
Make: Honda
Model: Civic
Year: 2021
Engine No: ENG123456789
Chassis No: CHS987654321

Coverage: Comprehensive
Sum Insured: PKR 3,500,000
```

This structured format ensures accurate data extraction!

---

## ❓ Need Help?

- Check logs: `docker compose logs backend | grep gmail`
- API documentation: http://localhost:8000/docs
- Test endpoint: http://localhost:8000/api/gmail/auth-url
- Google Cloud Console: https://console.cloud.google.com/

---

**Setup Complete! 🚀**
