"""
Gmail poller
APScheduler job that runs every 5 minutes
Fetches, classifies, and processes car insurance emails
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.gmail_service import (
    fetch_unread_emails,
    classify_email,
    extract_policy_data,
    mark_as_read
)
from app.models.policy import Policy, generate_policy_number, PolicyStatus
from app.models.client import Client, AddressType
from app.models.vehicle import Vehicle, RegistrationStatus, calculate_vehicle_age
from app.database import SessionLocal
import logging

logger = logging.getLogger(__name__)


async def run_gmail_poller():
    """
    Job function that polls Gmail inbox
    Runs every 5 minutes
    """
    logger.info("Starting Gmail poller...")
    
    db = SessionLocal()
    try:
        # Fetch unread emails
        emails = fetch_unread_emails()
        logger.info(f"Found {len(emails)} unread emails")
        
        for email in emails:
            try:
                # Classify email
                is_car_insurance = classify_email(email['subject'], email['body'])
                
                if is_car_insurance:
                    logger.info(f"Car insurance email detected: {email['subject']}")
                    
                    # Extract data
                    data = extract_policy_data(email['subject'], email['body'])
                    logger.info(f"Extracted data: {data}")
                    
                    if data.get('client_name'):
                        # Create or get client
                        client = db.query(Client).filter(Client.name == data['client_name']).first()
                        
                        if not client:
                            client = Client(
                                name=data['client_name'],
                                address_type=AddressType.HOME,
                                address="Address from email",
                                country="Pakistan",
                                city="Unknown",
                                email=data.get('email'),
                                phone1=data.get('phone')
                            )
                            db.add(client)
                            db.commit()
                            db.refresh(client)
                            logger.info(f"Created new client: {client.name}")
                        
                        # Create draft policy
                        policy = Policy(
                            policy_number=generate_policy_number(),
                            client_id=client.id,
                            policy_type="Motor Insurance",
                            status=PolicyStatus.DRAFT,
                            currency="PKR",
                            notes=f"Auto-created from email: {email['subject']}"
                        )
                        db.add(policy)
                        db.commit()
                        db.refresh(policy)
                        logger.info(f"Created draft policy: {policy.policy_number}")
                        
                        # Create vehicle if data available
                        if data.get('make') or data.get('engine_no'):
                            vehicle = Vehicle(
                                policy_id=policy.id,
                                registration_status=RegistrationStatus.REGISTERED,
                                make=data.get('make'),
                                model=data.get('model'),
                                year_of_manufacturing=data.get('year'),
                                vehicle_age=calculate_vehicle_age(data['year']) if data.get('year') else None,
                                engine_no=data.get('engine_no'),
                                chassis_no=data.get('chassis_no')
                            )
                            db.add(vehicle)
                            db.commit()
                            logger.info(f"Created vehicle for policy {policy.policy_number}")
                    
                    # Mark email as read
                    mark_as_read(email['id'])
                    logger.info(f"Marked email as read: {email['id']}")
                else:
                    logger.info(f"Email not related to car insurance: {email['subject']}")
                    
            except Exception as e:
                logger.error(f"Error processing email {email.get('id')}: {e}")
        
        logger.info("Gmail poller completed")
        
    except Exception as e:
        logger.error(f"Error in Gmail poller: {e}")
    finally:
        db.close()


def setup_gmail_poller(scheduler: AsyncIOScheduler):
    """
    Set up Gmail poller job in scheduler
    Runs every 5 minutes
    
    Args:
        scheduler: APScheduler instance
    """
    scheduler.add_job(
        run_gmail_poller,
        'interval',
        minutes=5,
        id='gmail_poller',
        replace_existing=True
    )
    logger.info("Gmail poller scheduled: Every 5 minutes")
