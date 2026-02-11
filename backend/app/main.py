"""
FastAPI main application
Entry point for IGI Insurance Automation System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db
from app.automation.scheduler import scheduler, start_scheduler
from app.automation.reminder_job import setup_reminder_job
from app.automation.gmail_poller import setup_gmail_poller
import logging

# Import all routers
from app.routers.clients import router as clients_router
from app.routers.policies import router as policies_router
from app.routers.banks import banks, product_setup, items, perils
from app.routers.vehicles import vehicles, discounts, policy_discounts, deductibles, clauses, warranties, agencies
from app.routers.final_policy import computational_sheet, final_policy, reminders, gmail_integration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("Starting IGI Insurance Automation System...")
    
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Start scheduler
    start_scheduler()
    
    # Set up jobs
    setup_reminder_job(scheduler)
    setup_gmail_poller(scheduler)
    
    logger.info("Scheduler started with jobs")
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    if scheduler.running:
        scheduler.shutdown()
    logger.info("Scheduler stopped")


# Create FastAPI app
app = FastAPI(
    title="IGI Insurance Automation API",
    description="Complete backend-driven insurance automation system for IGI Insurance",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - more permissive for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default port
        "http://frontend:3000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clients_router)
app.include_router(policies_router)
app.include_router(banks)
app.include_router(product_setup)
app.include_router(items)
app.include_router(perils)
app.include_router(vehicles)
app.include_router(discounts)
app.include_router(policy_discounts)
app.include_router(deductibles)
app.include_router(clauses)
app.include_router(warranties)
app.include_router(agencies)
app.include_router(computational_sheet)
app.include_router(final_policy)
app.include_router(reminders)
app.include_router(gmail_integration)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "IGI Insurance Automation API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "scheduler_running": scheduler.running
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
