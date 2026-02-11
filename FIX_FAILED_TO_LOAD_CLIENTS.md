# Fix: "Failed to Load Clients" Error

## Problem
When opening the Clients module, you see an error message: **"Failed to load clients"**

## Common Causes & Solutions

### 1. Backend Not Running ✅ MOST COMMON

**Symptom:** Error message: "Cannot connect to server. Please ensure the backend is running."

**Solution:**
```bash
# Make sure Docker services are running
docker compose up --build

# Or if already running, restart:
docker compose restart backend

# Check if backend is accessible:
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "scheduler_running": true
}
```

---

### 2. Database Not Initialized

**Symptom:** Backend starts but API returns 500 errors

**Solution:**
```bash
# Restart backend to trigger database initialization
docker compose restart backend

# Check backend logs:
docker compose logs backend | grep "Database initialized"
```

**Expected Log:**
```
backend-1  | INFO:     Database initialized
```

---

### 3. CORS Issues

**Symptom:** Browser console shows CORS errors

**Solution:**
- ✅ Already fixed in the code!
- Backend now accepts requests from:
  - http://localhost:3000
  - http://localhost:5173 (Vite default)
  - http://frontend:3000 (Docker)
  - http://127.0.0.1:3000
  - http://127.0.0.1:5173

---

### 4. API URL Configuration

**Symptom:** Frontend trying to connect to wrong URL

**Solution:**
- ✅ Already fixed in the code!
- Frontend now uses Vite proxy (relative URLs)
- No need to set `VITE_API_BASE_URL` environment variable

---

### 5. Port Conflicts

**Symptom:** Services fail to start

**Solution:**
```bash
# Check if ports are already in use
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL

# If ports are in use, stop conflicting services or change ports in docker-compose.yml
```

---

## Quick Fix Steps

### Step 1: Ensure Services Are Running
```bash
cd igi-insurance-automation
docker compose up --build
```

Wait for all services to start:
- ✅ PostgreSQL (port 5432)
- ✅ Backend (port 8000)
- ✅ Frontend (port 3000)

### Step 2: Verify Backend Health
```bash
# Test backend directly
curl http://localhost:8000/health

# Test clients endpoint
curl http://localhost:8000/api/clients/
```

**Expected Response:**
```json
[]
```
(Empty array is OK if no clients exist yet)

### Step 3: Open Frontend
```bash
# Open in browser
http://localhost:3000
```

### Step 4: Navigate to Clients
1. Click **"Clients"** in the sidebar
2. Should see either:
   - Empty table with message: "No clients found. Click 'Add New Client' to create one."
   - OR list of existing clients

---

## Improved Error Messages

The code now shows better error messages:

### Before:
```
Failed to load clients
```

### After:
```
Cannot connect to server. Please ensure the backend is running.
[🔄 Retry Connection] Make sure backend is running: docker compose up
```

---

## Testing the Fix

### Test 1: Backend Connection
```bash
# In terminal
curl http://localhost:8000/api/clients/
```

**Success:** Returns `[]` or list of clients
**Failure:** Connection refused → Backend not running

### Test 2: Frontend Access
1. Open http://localhost:3000
2. Click "Clients"
3. Should NOT see "Failed to load clients" error
4. Should see either empty table or list of clients

### Test 3: Create a Client
1. Click "+ Add New Client"
2. Fill in required fields:
   - Name: Test Client
   - Address Type: Home
   - Address: 123 Test St
   - Country: Pakistan
   - City: Karachi
3. Click "Create Client"
4. Should see success message
5. Should see client in the table

---

## Debugging Tips

### Check Browser Console
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for errors:
   - ❌ `ERR_CONNECTION_REFUSED` → Backend not running
   - ❌ `CORS error` → Already fixed, restart backend
   - ❌ `404 Not Found` → Wrong API endpoint
   - ❌ `500 Internal Server Error` → Backend error, check logs

### Check Backend Logs
```bash
# See all backend logs
docker compose logs backend

# Follow logs in real-time
docker compose logs -f backend

# Check for errors
docker compose logs backend | grep ERROR
```

### Check Network Tab
1. Open DevTools → Network tab
2. Reload page or click Clients
3. Look for request to `/api/clients/`
4. Check:
   - Status: Should be 200 OK
   - Response: Should be JSON array
   - Time: Should be < 1 second

---

## What Was Fixed

### 1. API Client (frontend/src/api/index.ts)
- ✅ Changed to use relative URLs (empty string)
- ✅ Added 10-second timeout
- ✅ Leverages Vite's proxy configuration

### 2. CORS Configuration (backend/app/main.py)
- ✅ Added more allowed origins
- ✅ Includes localhost:5173 (Vite default)
- ✅ Includes 127.0.0.1 variants

### 3. Error Handling (frontend/src/components/forms/ClientsForm.tsx)
- ✅ Better error messages
- ✅ Distinguishes between connection errors and server errors
- ✅ Shows "Retry Connection" button when backend is unreachable
- ✅ Provides actionable guidance

---

## Prevention

To avoid this error in the future:

1. **Always start services with Docker Compose:**
   ```bash
   docker compose up --build
   ```

2. **Check service health before using:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Monitor logs during development:**
   ```bash
   docker compose logs -f
   ```

4. **Keep services running while developing:**
   - Don't stop Docker services unnecessarily
   - Use `docker compose restart` instead of down/up

---

## Still Having Issues?

If you still see "Failed to load clients" after following all steps:

1. **Check Docker Services:**
   ```bash
   docker compose ps
   ```
   All should show "Up" status

2. **Full Reset:**
   ```bash
   # Stop everything
   docker compose down -v
   
   # Remove all data (WARNING: deletes database)
   docker system prune -a --volumes
   
   # Start fresh
   docker compose up --build
   ```

3. **Check System Resources:**
   - Ensure Docker has enough memory (4GB+ recommended)
   - Ensure ports 3000, 8000, 5432 are available

4. **Review Documentation:**
   - GETTING_STARTED.md
   - TROUBLESHOOTING.md
   - README.md

---

## Summary

**Problem:** "Failed to load clients" error
**Root Cause:** Multiple potential issues (backend not running, CORS, API config)
**Solution:** Fixed API configuration, CORS, and improved error messages
**Result:** Better error messages guide users to fix the issue themselves

**Status: FIXED ✅**
