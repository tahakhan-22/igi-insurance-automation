# 🎯 Quick Reference - Common Commands

Quick reference for the most commonly used commands when working with the IGI Insurance Automation system.

## 🚀 Starting & Stopping

```bash
# Start all services (first time or after changes)
docker compose up --build

# Start all services (subsequent runs)
docker compose up

# Start in detached mode (background)
docker compose up -d

# Stop all services (Ctrl+C or)
docker compose down

# Stop and remove all data including database
docker compose down -v
```

## 📊 Monitoring & Logs

```bash
# View all logs
docker compose logs

# View specific service logs
docker compose logs backend
docker compose logs frontend
docker compose logs db

# Follow logs in real-time
docker compose logs -f backend

# Check service status
docker compose ps

# Check backend health
curl http://localhost:8000/health
```

## 🔄 Updates & Rebuilds

```bash
# Pull latest code
git pull origin main

# Rebuild after code changes
docker compose down
docker compose up --build

# Rebuild specific service
docker compose up --build backend

# Restart a specific service
docker compose restart backend
```

## 🗄️ Database Operations

```bash
# Access PostgreSQL shell
docker compose exec db psql -U postgres -d igi_insurance

# Common SQL commands
\dt              # List all tables
\d table_name    # Describe table structure
SELECT * FROM clients LIMIT 10;  # Query data

# Backup database
docker compose exec db pg_dump -U postgres igi_insurance > backup.sql

# Restore database
docker compose exec -T db psql -U postgres igi_insurance < backup.sql
```

## 🐛 Debugging

```bash
# Access backend container shell
docker compose exec backend bash

# Access frontend container shell
docker compose exec frontend sh

# Run Python commands in backend
docker compose exec backend python -c "from app.database import engine; print(engine)"

# Check Python packages
docker compose exec backend pip list

# Check Node packages
docker compose exec frontend npm list
```

## 🧹 Cleanup

```bash
# Remove stopped containers
docker compose rm

# Clean up Docker system
docker system prune

# Remove all unused images
docker image prune -a

# Full cleanup (be careful!)
docker compose down -v
docker system prune -a -f
```

## 🔧 Development

```bash
# Backend - Install new Python package
docker compose exec backend pip install package-name
# Then add to requirements.txt

# Frontend - Install new npm package
docker compose exec frontend npm install package-name

# Run backend tests (if available)
docker compose exec backend pytest

# Format Python code
docker compose exec backend black .

# Lint Python code
docker compose exec backend pylint app/
```

## 📡 API Testing

```bash
# Health check
curl http://localhost:8000/health

# List all clients
curl http://localhost:8000/api/clients/

# Create a client (example)
curl -X POST http://localhost:8000/api/clients/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Client",
    "address_type": "Home",
    "address": "123 Test St",
    "country": "Pakistan",
    "city": "Karachi"
  }'

# Trigger payment reminders manually
curl -X POST http://localhost:8000/api/reminders/trigger

# Or use the interactive API docs
open http://localhost:8000/docs
```

## 🌐 Access Points

```bash
# Frontend Application
http://localhost:3000

# Backend API
http://localhost:8000

# Interactive API Documentation
http://localhost:8000/docs

# Alternative API Documentation
http://localhost:8000/redoc

# Health Check Endpoint
http://localhost:8000/health

# PostgreSQL Database
postgresql://postgres:postgres@localhost:5432/igi_insurance
```

## 📝 Environment Variables

```bash
# View current environment
cat .env

# Edit environment
nano .env
# or
code .env

# After changing .env, restart services
docker compose restart
```

## 🔐 Security

```bash
# Generate a secure secret key (for SECRET_KEY in .env)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or
openssl rand -base64 32
```

## 📦 Backup & Export

```bash
# Export Docker images
docker save -o igi-backend.tar igi-insurance-automation-backend
docker save -o igi-frontend.tar igi-insurance-automation-frontend

# Import Docker images
docker load -i igi-backend.tar
docker load -i igi-frontend.tar

# Export database
docker compose exec db pg_dump -U postgres igi_insurance > backup_$(date +%Y%m%d).sql
```

## 🆘 Emergency Recovery

```bash
# If services won't start
docker compose down -v
docker system prune -a
docker compose up --build

# If database is corrupted
docker compose down -v  # WARNING: This deletes all data
docker compose up --build

# If port conflicts
# Edit docker-compose.yml to change ports
# Example: Change 8000:8000 to 8001:8000
```

## 💡 Pro Tips

```bash
# Tail logs from all services
docker compose logs -f

# Execute any command in a running container
docker compose exec backend python app/scripts/your_script.py

# Check resource usage
docker stats

# See what's using a port (if conflicts occur)
# Linux/Mac:
lsof -i :3000
# Windows:
netstat -ano | findstr :3000

# Quick restart after code changes (no rebuild needed)
docker compose restart backend
docker compose restart frontend
```

## 📚 Related Documentation

- [Getting Started Guide](GETTING_STARTED.md) - Detailed setup instructions
- [README.md](README.md) - Project overview and features
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Technical details

---

**💡 Tip:** Bookmark this page for quick reference!

For more detailed information, refer to the [Getting Started Guide](GETTING_STARTED.md).
