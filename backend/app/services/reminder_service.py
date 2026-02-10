"""
Reminder service
Handles CSV parsing and reminder processing
"""
import csv
from datetime import datetime, date, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.reminder import Reminder
from app.services.email_service import send_reminder_email
from app.services.sms_service import send_reminder_sms
import logging
import os

logger = logging.getLogger(__name__)


def load_csv_reminders(csv_path: str) -> List[Dict]:
    """
    Parse CSV file and return list of reminder records
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        List of reminder dictionaries
    """
    reminders = []
    
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse due_date
                due_date = datetime.strptime(row['due_date'], '%Y-%m-%d').date()
                
                reminders.append({
                    'client_name': row['client_name'],
                    'email': row['email'],
                    'phone': row['phone'],
                    'due_amount': float(row['due_amount']),
                    'due_date': due_date
                })
    except Exception as e:
        logger.error(f"Error loading CSV reminders: {e}")
    
    return reminders


def get_upcoming_dues(reminders: List[Dict], days_ahead: int = 30) -> List[Dict]:
    """
    Filter reminders with due_date within next N days
    
    Args:
        reminders: List of reminder dictionaries
        days_ahead: Number of days ahead to check
        
    Returns:
        Filtered list of upcoming reminders
    """
    today = date.today()
    cutoff_date = today + timedelta(days=days_ahead)
    
    upcoming = []
    for reminder in reminders:
        due_date = reminder['due_date']
        if today <= due_date <= cutoff_date:
            upcoming.append(reminder)
    
    return upcoming


async def process_reminders(db: Session, csv_path: str = None) -> Dict[str, int]:
    """
    Main function: load CSV, find upcoming dues, send emails/SMS, mark as sent
    
    Args:
        db: Database session
        csv_path: Path to CSV file (defaults to app/data/due_payments.csv)
        
    Returns:
        Dictionary with processing stats
    """
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "due_payments.csv")
    
    if not os.path.exists(csv_path):
        logger.warning(f"CSV file not found: {csv_path}")
        return {"total": 0, "sent": 0, "failed": 0}
    
    # Load reminders from CSV
    reminders = load_csv_reminders(csv_path)
    logger.info(f"Loaded {len(reminders)} reminders from CSV")
    
    # Get upcoming dues (within 30 days)
    upcoming = get_upcoming_dues(reminders, days_ahead=30)
    logger.info(f"Found {len(upcoming)} upcoming dues")
    
    sent_count = 0
    failed_count = 0
    
    for reminder_data in upcoming:
        try:
            # Check if reminder already sent recently (within 7 days)
            existing = db.query(Reminder).filter(
                Reminder.client_name == reminder_data['client_name'],
                Reminder.due_date == reminder_data['due_date'],
                Reminder.reminder_sent == True
            ).first()
            
            if existing and existing.last_reminder_at:
                days_since = (datetime.now() - existing.last_reminder_at).days
                if days_since < 7:
                    logger.info(f"Skipping {reminder_data['client_name']} - reminder sent {days_since} days ago")
                    continue
            
            # Send email
            email_sent = False
            if reminder_data['email']:
                email_sent = await send_reminder_email(
                    reminder_data['email'],
                    reminder_data['client_name'],
                    reminder_data['due_amount'],
                    reminder_data['due_date'].strftime('%Y-%m-%d')
                )
            
            # Send SMS
            sms_sent = False
            if reminder_data['phone']:
                sms_sent = send_reminder_sms(
                    reminder_data['phone'],
                    reminder_data['client_name'],
                    reminder_data['due_amount'],
                    reminder_data['due_date'].strftime('%Y-%m-%d')
                )
            
            # Save or update reminder record
            if existing:
                existing.reminder_sent = True
                existing.last_reminder_at = datetime.now()
            else:
                new_reminder = Reminder(
                    client_name=reminder_data['client_name'],
                    email=reminder_data['email'],
                    phone=reminder_data['phone'],
                    due_amount=reminder_data['due_amount'],
                    due_date=reminder_data['due_date'],
                    reminder_sent=True,
                    last_reminder_at=datetime.now()
                )
                db.add(new_reminder)
            
            db.commit()
            
            if email_sent or sms_sent:
                sent_count += 1
                logger.info(f"Reminder sent to {reminder_data['client_name']}")
            else:
                failed_count += 1
                logger.warning(f"Failed to send reminder to {reminder_data['client_name']}")
                
        except Exception as e:
            failed_count += 1
            logger.error(f"Error processing reminder for {reminder_data['client_name']}: {e}")
    
    return {
        "total": len(upcoming),
        "sent": sent_count,
        "failed": failed_count
    }
