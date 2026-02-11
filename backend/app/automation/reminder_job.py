"""
Reminder job
APScheduler job that runs daily at 8:00 AM
Processes CSV due-payment reminders
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.reminder_service import process_reminders
from app.database import SessionLocal
import logging

logger = logging.getLogger(__name__)


async def run_reminder_job():
    """
    Job function that processes reminders
    Runs daily at 8:00 AM
    """
    logger.info("Starting reminder job...")
    
    db = SessionLocal()
    try:
        result = await process_reminders(db)
        logger.info(f"Reminder job completed: {result}")
    except Exception as e:
        logger.error(f"Error in reminder job: {e}")
    finally:
        db.close()


def setup_reminder_job(scheduler: AsyncIOScheduler):
    """
    Set up reminder job in scheduler
    Runs daily at 8:00 AM
    
    Args:
        scheduler: APScheduler instance
    """
    scheduler.add_job(
        run_reminder_job,
        'cron',
        hour=8,
        minute=0,
        id='reminder_job',
        replace_existing=True
    )
    logger.info("Reminder job scheduled: Daily at 8:00 AM")
