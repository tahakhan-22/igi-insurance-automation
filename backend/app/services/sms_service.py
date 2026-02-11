"""
SMS service
Mock implementation - logs to console and file
Ready for real gateway integration
"""
import logging
from datetime import datetime
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_reminder_sms(phone: str, client_name: str, due_amount: float, due_date: str) -> bool:
    """
    Send reminder SMS
    Mock implementation: logs the message to console and file
    Ready for real gateway integration
    
    Args:
        phone: Phone number
        client_name: Client name
        due_amount: Amount due
        due_date: Due date
        
    Returns:
        True (mock always succeeds)
    """
    message = f"Dear {client_name}, Reminder: Your payment of PKR {due_amount:,.2f} is due on {due_date}. Please contact IGI Insurance for payment. Thank you."
    
    # Log to console
    logger.info(f"SMS to {phone}: {message}")
    
    # Log to file
    try:
        with open("/tmp/sms_log.txt", "a") as f:
            f.write(f"[{datetime.now().isoformat()}] To: {phone} | Message: {message}\n")
    except Exception as e:
        logger.error(f"Error writing SMS log: {e}")
    
    # In production, replace with real SMS gateway API call
    # Example:
    # response = requests.post(
    #     settings.SMS_GATEWAY_URL,
    #     headers={"Authorization": f"Bearer {settings.SMS_API_KEY}"},
    #     json={"phone": phone, "message": message}
    # )
    # return response.status_code == 200
    
    return True
