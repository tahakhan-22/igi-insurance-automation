"""
Gmail service
Gmail API with OAuth 2.0 for email reading and classification
"""
import os
import re
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import base64
from app.config import settings
import logging

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']


def get_auth_url() -> str:
    """
    Generate OAuth 2.0 authorization URL for Gmail API
    
    Returns:
        Authorization URL string
    """
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GMAIL_CLIENT_ID,
                "client_secret": settings.GMAIL_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GMAIL_REDIRECT_URI]
            }
        },
        scopes=SCOPES,
        redirect_uri=settings.GMAIL_REDIRECT_URI
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent')
    return auth_url


def handle_oauth_callback(code: str) -> Dict:
    """
    Exchange auth code for tokens, store securely
    
    Args:
        code: Authorization code from OAuth callback
        
    Returns:
        Token dictionary
    """
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GMAIL_CLIENT_ID,
                "client_secret": settings.GMAIL_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GMAIL_REDIRECT_URI]
            }
        },
        scopes=SCOPES,
        redirect_uri=settings.GMAIL_REDIRECT_URI
    )
    
    flow.fetch_token(code=code)
    creds = flow.credentials
    
    # Save credentials
    token_path = '/tmp/gmail_token.pickle'
    with open(token_path, 'wb') as token:
        pickle.dump(creds, token)
    
    return {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes
    }


def get_gmail_service():
    """
    Build Gmail API service using stored credentials
    
    Returns:
        Gmail API service object
    """
    creds = None
    token_path = '/tmp/gmail_token.pickle'
    
    # Load credentials from file
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh if expired
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    if not creds or not creds.valid:
        raise Exception("No valid credentials. Please authenticate first.")
    
    return build('gmail', 'v1', credentials=creds)


def fetch_unread_emails() -> List[Dict]:
    """
    Fetch unread emails from inbox
    
    Returns:
        List of email dictionaries
    """
    try:
        service = get_gmail_service()
        
        # Get unread messages
        results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=10
        ).execute()
        
        messages = results.get('messages', [])
        emails = []
        
        for message in messages:
            # Get message details
            msg = service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()
            
            # Extract subject and body
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            
            # Extract body
            body = ""
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
            elif 'body' in msg['payload'] and 'data' in msg['payload']['body']:
                body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
            
            emails.append({
                'id': message['id'],
                'subject': subject,
                'body': body
            })
        
        return emails
    
    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        return []


def mark_as_read(message_id: str) -> bool:
    """
    Mark email as read after processing
    
    Args:
        message_id: Gmail message ID
        
    Returns:
        True if successful, False otherwise
    """
    try:
        service = get_gmail_service()
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        return True
    except Exception as e:
        logger.error(f"Error marking email as read: {e}")
        return False


def classify_email(subject: str, body: str) -> bool:
    """
    Keyword-based classification
    Returns True if email is related to car/motor insurance
    
    Args:
        subject: Email subject
        body: Email body
        
    Returns:
        True if car insurance related, False otherwise
    """
    keywords = [
        'car insurance', 'motor insurance', 'vehicle policy', 'motor policy',
        'registration', 'chassis', 'engine number', 'sum insured', 'premium',
        'vehicle insurance', 'auto insurance', 'comprehensive cover',
        'motor vehicle', 'car policy'
    ]
    
    text = (subject + " " + body).lower()
    
    return any(keyword in text for keyword in keywords)


def extract_policy_data(subject: str, body: str) -> Dict:
    """
    Extract client & vehicle details from email body using regex patterns
    
    Args:
        subject: Email subject
        body: Email body
        
    Returns:
        Dictionary with extracted data
    """
    data = {}
    
    # Name patterns
    name_match = re.search(r'(?:name|client|insured):\s*([A-Za-z\s]+)', body, re.IGNORECASE)
    if name_match:
        data['client_name'] = name_match.group(1).strip()
    
    # Make pattern
    make_match = re.search(r'make:\s*([A-Za-z\s]+)', body, re.IGNORECASE)
    if make_match:
        data['make'] = make_match.group(1).strip()
    
    # Model pattern
    model_match = re.search(r'model:\s*([A-Za-z0-9\s]+)', body, re.IGNORECASE)
    if model_match:
        data['model'] = model_match.group(1).strip()
    
    # Year pattern
    year_match = re.search(r'year:\s*(\d{4})', body, re.IGNORECASE)
    if year_match:
        data['year'] = int(year_match.group(1))
    
    # Engine number pattern
    engine_match = re.search(r'engine(?:\s+(?:no|number))?:\s*([A-Z0-9]+)', body, re.IGNORECASE)
    if engine_match:
        data['engine_no'] = engine_match.group(1).strip()
    
    # Chassis number pattern
    chassis_match = re.search(r'chassis(?:\s+(?:no|number))?:\s*([A-Z0-9]+)', body, re.IGNORECASE)
    if chassis_match:
        data['chassis_no'] = chassis_match.group(1).strip()
    
    # Email pattern
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', body)
    if email_match:
        data['email'] = email_match.group(0)
    
    # Phone pattern (Pakistani)
    phone_match = re.search(r'(?:\+92|0)?3[0-9]{9}', body)
    if phone_match:
        data['phone'] = phone_match.group(0)
    
    # Sum insured pattern
    value_match = re.search(r'(?:sum\s+insured|value):\s*(?:PKR|Rs\.?)?\s*([\d,]+)', body, re.IGNORECASE)
    if value_match:
        data['sum_insured'] = float(value_match.group(1).replace(',', ''))
    
    return data
