# 🔧 Troubleshooting Guide

Common issues and solutions for the IGI Insurance Automation system.

## Docker Build Issues

### Package Installation Errors

**Error:** `E: Package 'libgdk-pixbuf2.0-0' has no installation candidate`

**Cause:** Outdated package name in Dockerfile for newer Debian versions.

**Solution:**
```bash
# Pull the latest code with fixes
git pull origin main

# Clean Docker cache and rebuild
docker compose down -v
docker system prune -a
docker compose up --build
```

The issue has been fixed in the latest version by updating the package name from `libgdk-pixbuf2.0-0` to `libgdk-pixbuf-2.0-0`.

### Docker Compose Version Warning

**Warning:** `the attribute 'version' is obsolete`

**Cause:** Docker Compose v2 no longer requires the version field.

**Solution:** This is just a warning and doesn't affect functionality. The latest `docker-compose.yml` has this field removed.

## Windows-Specific Issues

### PowerShell Path Errors

**Error:** `cd : Cannot find path 'C:\Users\...\igi-insurance-automation\igi-insurance-automation'`

**Cause:** Trying to navigate into a subdirectory that doesn't exist. After cloning, you're already in the correct directory.

**Solution:**
```powershell
# After cloning, you're already in the right directory
git clone https://github.com/tahakhan-22/igi-insurance-automation.git
cd igi-insurance-automation

# DON'T do this:
# cd igi-insurance-automation  (❌ This tries to go into a non-existent subdirectory)

# You're ready to run commands:
cp .env.example .env
docker compose up --build
```

**Check your current directory:**
```powershell
# PowerShell
pwd

# Should show something like:
# C:\Users\YourName\Desktop\igi-insurance-automation
```

### Line Endings (CRLF vs LF)

**Error:** Shell scripts fail with `\r` errors

**Solution:**
```bash
# Configure Git to handle line endings
git config --global core.autocrlf true
```

### Docker Desktop Not Running

**Error:** `Cannot connect to the Docker daemon`

**Solution:**
1. Open Docker Desktop
2. Wait for it to fully start (whale icon in system tray)
3. Run your docker compose command again

### WSL2 Backend Required

**Error:** Docker Desktop requires WSL2

**Solution:**
1. Install WSL2: `wsl --install`
2. Restart your computer
3. Open Docker Desktop settings
4. Enable "Use WSL2 based engine"

## Port Conflicts

### Port Already in Use

**Error:** `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Check what's using the port:**

**Windows (PowerShell):**
```powershell
netstat -ano | findstr :3000
netstat -ano | findstr :8000
netstat -ano | findstr :5432

# To stop a process by PID (replace 1234 with actual PID)
taskkill /PID 1234 /F
```

**Mac/Linux:**
```bash
lsof -i :3000
lsof -i :8000
lsof -i :5432
```

**Alternative solution:** Change ports in `docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Change external port from 8000 to 8001
```

## Database Issues

### Database Connection Failed

**Error:** `could not connect to server: Connection refused`

**Solution:**
```bash
# Check if database is running
docker compose ps

# Database should show "healthy" status
# If not, check logs
docker compose logs db

# Restart database
docker compose restart db
```

### Database Already Exists Error

**Error:** `database "igi_insurance" already exists`

**Solution:** This is usually harmless. The database persists across restarts. To start fresh:
```bash
# Remove all data and start clean (⚠️ This deletes all data)
docker compose down -v
docker compose up --build
```

## Frontend Issues

### Node Modules Not Found

**Error:** `Cannot find module 'react'`

**Solution:**
```bash
# Rebuild frontend container
docker compose down
docker compose up --build frontend
```

### Frontend Not Loading

1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check frontend logs:**
   ```bash
   docker compose logs frontend
   ```

3. **Clear browser cache:**
   - Press `Ctrl+Shift+Delete`
   - Clear cached images and files
   - Reload page

## Backend Issues

### Python Import Errors

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:**
```bash
# Rebuild backend with dependencies
docker compose down
docker compose up --build backend
```

### WeasyPrint Rendering Issues

**Error:** Font or rendering problems in PDF generation

**Solution:** The latest Dockerfile includes all required WeasyPrint dependencies. Make sure you're using the latest code:
```bash
git pull origin main
docker compose up --build backend
```

## Environment Configuration

### Missing .env File

**Error:** `env file not found`

**Solution:**
```bash
# Create .env from template
cp .env.example .env

# Edit with your settings (optional for basic testing)
```

### Database URL Wrong

**Error:** Database connection fails

**Solution:** Make sure your `.env` has the correct URL:
```env
# For Docker (default)
DATABASE_URL=postgresql://postgres:postgres@db:5432/igi_insurance

# For local PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/igi_insurance
```

## Performance Issues

### Slow Build Times

**Solution:**
```bash
# Use BuildKit for faster builds (Windows PowerShell)
$env:DOCKER_BUILDKIT=1
docker compose up --build

# Mac/Linux
export DOCKER_BUILDKIT=1
docker compose up --build
```

### High CPU/Memory Usage

**Solution:**
1. Open Docker Desktop settings
2. Adjust Resources (CPU/Memory limits)
3. Recommended: 4 CPU cores, 8GB RAM

## Network Issues

### Cannot Pull Docker Images

**Error:** `Error response from daemon: Get https://...`

**Solution:**
1. Check internet connection
2. If behind proxy, configure Docker proxy settings
3. Try different network (corporate networks may block Docker Hub)

### DNS Resolution Failed

**Error:** `Could not resolve 'deb.debian.org'`

**Solution:**
```bash
# Add DNS servers to Docker
# Edit Docker Desktop settings
# DNS: 8.8.8.8, 8.8.4.4
```

## Getting More Help

### Enable Debug Logging

```bash
# View all logs
docker compose logs

# Follow logs in real-time
docker compose logs -f

# View specific service logs
docker compose logs backend
docker compose logs frontend
docker compose logs db
```

### Check Container Status

```bash
# List all containers
docker compose ps

# Inspect a specific container
docker compose exec backend bash
docker compose exec frontend sh
```

### Clean Slate Restart

If nothing else works, start completely fresh:

```bash
# Stop and remove everything
docker compose down -v

# Remove all Docker images (⚠️ Nuclear option)
docker system prune -a --volumes

# Pull latest code
git pull origin main

# Start fresh
docker compose up --build
```

## Still Having Issues?

1. Check if your issue is listed in [GETTING_STARTED.md](GETTING_STARTED.md#-troubleshooting)
2. Review the [Quick Reference](QUICK_REFERENCE.md) for common commands
3. Check Docker Desktop logs (Settings > Troubleshoot > Open logs folder)
4. Create an issue on GitHub with:
   - Your operating system
   - Docker version: `docker --version`
   - Docker Compose version: `docker compose version`
   - Error messages (full output)
   - Steps to reproduce

## Useful Commands for Debugging

```bash
# Check Docker version
docker --version
docker compose version

# Check disk space
docker system df

# View Docker system info
docker info

# Check running containers
docker ps

# Check all containers (including stopped)
docker ps -a

# View container resource usage
docker stats

# Test database connection
docker compose exec db psql -U postgres -d igi_insurance -c "SELECT 1"

# Test backend health
curl http://localhost:8000/health
```

---

**💡 Tip:** Most issues can be resolved by pulling the latest code and rebuilding:
```bash
git pull origin main
docker compose down -v
docker compose up --build
```
