"""
Email service
Sends emails via SMTP
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os
from app.config import settings


async def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """
    Send email via SMTP
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of email
        
    Returns:
        True if sent successfully, False otherwise
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["From"] = settings.SMTP_USER
        message["To"] = to_email
        message["Subject"] = subject
        
        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True
        )
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


async def send_reminder_email(to_email: str, client_name: str, due_amount: float, due_date: str) -> bool:
    """
    Send reminder email using template
    
    Args:
        to_email: Recipient email address
        client_name: Client name
        due_amount: Amount due
        due_date: Due date
        
    Returns:
        True if sent successfully, False otherwise
    """
    # Load template
    template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("reminder_email.html")
    
    # Render template
    html_content = template.render(
        client_name=client_name,
        due_amount=due_amount,
        due_date=due_date
    )
    
    # Send email
    subject = f"Payment Reminder - IGI Insurance - Due: PKR {due_amount:,.2f}"
    return await send_email(to_email, subject, html_content)
