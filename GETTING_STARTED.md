# 🚀 Getting Started with IGI Insurance Automation

This guide will help you set up and run the IGI Insurance Automation system on your local machine after cloning the repository.

## 📋 Prerequisites

Before you begin, make sure you have the following installed on your system:

### Required
- **Docker Desktop** (recommended for easiest setup)
  - Windows/Mac: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
  - Linux: [Install Docker Engine](https://docs.docker.com/engine/install/)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Optional (for local development without Docker)
- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **PostgreSQL 15+** - [Download PostgreSQL](https://www.postgresql.org/download/)

## 🎯 Quick Start (Recommended - Using Docker)

This is the easiest way to get started. Docker will handle all dependencies automatically.

### Step 1: Clone the Repository

If you haven't already cloned the repository:

```bash
git clone https://github.com/tahakhan-22/igi-insurance-automation.git
cd igi-insurance-automation
```

### Step 2: Configure Environment Variables

Create your environment configuration file:

```bash
# Copy the example environment file
cp .env.example .env
```

**Important:** Open the `.env` file and update the following variables (minimum required):

```env
# Database (default values work with Docker)
DATABASE_URL=postgresql://postgres:postgres@db:5432/igi_insurance

# Email Configuration (optional for testing, required for email features)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Gmail API (optional, only needed for Gmail integration)
GMAIL_CLIENT_ID=your-google-client-id
GMAIL_CLIENT_SECRET=your-google-client-secret

# Security (change this to a random string)
SECRET_KEY=your-random-secret-key-here-change-this
```

> 💡 **Tip:** For initial testing, you can leave the default values. Email and Gmail features will be mocked.

### Step 3: Start the Application

Run this single command to start everything:

```bash
docker compose up --build
```

This will:
- Download and set up PostgreSQL database
- Build and start the backend (Python/FastAPI)
- Build and start the frontend (React/TypeScript)
- Initialize the database with tables
- Start automation jobs (reminders and Gmail polling)

**First-time startup:** The build process may take 3-5 minutes. Subsequent starts will be much faster.

### Step 4: Access the Application

Once you see log messages indicating the services are running, open your browser:

- **Frontend (Main Application):** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Step 5: Verify Everything is Working

1. Open http://localhost:8000/health in your browser
   - You should see: `{"status":"healthy","scheduler_running":true}`

2. Open http://localhost:8000/docs
   - You should see the interactive API documentation (Swagger UI)

3. Open http://localhost:3000
   - You should see the IGI Insurance management interface

## 🛑 Stopping the Application

To stop all services:

```bash
# Press Ctrl+C in the terminal where docker compose is running
# OR run this command in another terminal:
docker compose down
```

To stop and remove all data (including database):

```bash
docker compose down -v
```

## 🔧 Local Development Setup (Without Docker)

If you prefer to run the services locally for development:

### Backend Setup

1. **Create a virtual environment:**
```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL:**
- Install PostgreSQL locally
- Create database: `createdb igi_insurance`
- Update DATABASE_URL in `.env` to point to your local PostgreSQL

4. **Run the backend:**
```bash
# Make sure you're in the backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Run the development server:**
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## 🎮 Using the Application

### First Steps

1. **Create a Client:**
   - Go to the Clients module in the sidebar
   - Click "New Client" (if form exists) or use the API at http://localhost:8000/docs

2. **Create a Policy:**
   - Go to Policies module
   - Click "New Policy"
   - Link it to a client

3. **Explore the API:**
   - Visit http://localhost:8000/docs
   - Try the interactive API endpoints
   - Create clients, policies, vehicles, etc.

### Testing Automation Features

#### CSV Payment Reminders
- Sample data is in `backend/app/data/due_payments.csv`
- Reminders run daily at 8:00 AM
- Test manually: POST to http://localhost:8000/api/reminders/trigger

#### Gmail Integration
- Requires Gmail API credentials
- Set up OAuth at Google Cloud Console
- Update GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET in `.env`
- Visit http://localhost:8000/api/gmail/auth-url to authenticate

## 🐛 Troubleshooting

### Port Already in Use

If you see errors about ports 3000, 8000, or 5432 being in use:

```bash
# Check what's using the port
# On Mac/Linux:
lsof -i :3000
lsof -i :8000
lsof -i :5432

# On Windows:
netstat -ano | findstr :3000
```

**Solution:** Either stop the conflicting service or change the ports in `docker-compose.yml`

### Docker Build Fails

```bash
# Clean up Docker and try again
docker compose down -v
docker system prune -a
docker compose up --build
```

### Database Connection Error

Make sure PostgreSQL is running:
```bash
docker compose ps
```

All services should show "healthy" or "running" status.

### Frontend Not Loading

1. Check if backend is running: http://localhost:8000/health
2. Check browser console for errors
3. Verify the API proxy is configured in `frontend/vite.config.ts`

### Import Errors in Backend

Make sure you're using Python 3.11+:
```bash
python --version
```

If using virtual environment, make sure it's activated.

## 📚 Next Steps

- **Read the API Documentation:** http://localhost:8000/docs
- **Check IMPLEMENTATION_SUMMARY.md** for technical details
- **Review SECURITY_FIXES.md** for security information
- **Explore the code:**
  - Backend: `backend/app/`
  - Frontend: `frontend/src/`
  - Models: `backend/app/models/`
  - API Routes: `backend/app/routers/`

## 🆘 Getting Help

If you encounter issues:

1. Check the logs:
   ```bash
   docker compose logs backend
   docker compose logs frontend
   docker compose logs db
   ```

2. Verify your environment:
   ```bash
   docker compose config
   ```

3. Check if all containers are running:
   ```bash
   docker compose ps
   ```

## 🔄 Updating the Application

To get the latest changes:

```bash
git pull origin main
docker compose down
docker compose up --build
```

## 💡 VS Code Tips

### Recommended Extensions
- **Python** by Microsoft
- **Pylance** by Microsoft
- **Docker** by Microsoft
- **ESLint** by Microsoft
- **TypeScript Vue Plugin (Volar)**

### Opening in VS Code
```bash
# From the project root
code .
```

### Running Docker from VS Code
1. Install the Docker extension
2. View Docker containers in the sidebar
3. Right-click on containers to start/stop/view logs

### Debugging
- Backend: Use the Python debugger
- Frontend: Use browser DevTools (F12)

---

**You're all set! 🎉** The system should now be running and accessible at http://localhost:3000

For detailed information about the system architecture and features, see the main README.md.
