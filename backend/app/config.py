from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/igi_insurance"
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    # Gmail API
    GMAIL_CLIENT_ID: str = ""
    GMAIL_CLIENT_SECRET: str = ""
    GMAIL_REDIRECT_URI: str = "http://localhost:8000/api/gmail/callback"
    
    # Security
    SECRET_KEY: str = "change-this-to-a-random-secret-key"
    
    # SMS
    SMS_GATEWAY_URL: str = "mock"
    SMS_API_KEY: str = "mock"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
