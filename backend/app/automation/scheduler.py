"""
APScheduler setup
Configures background job scheduler
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure scheduler
jobstores = {
    'default': MemoryJobStore()
}

executors = {
    'default': {'type': 'threadpool', 'max_workers': 20}
}

job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone='Asia/Karachi'
)


def start_scheduler():
    """Start the scheduler"""
    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler started successfully")
