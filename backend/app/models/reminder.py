from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    due_amount = Column(Numeric(15, 2), nullable=False)
    due_date = Column(Date, nullable=False)
    reminder_sent = Column(Boolean, default=False)
    last_reminder_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
