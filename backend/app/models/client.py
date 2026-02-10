from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class AddressType(str, enum.Enum):
    HOME = "Home"
    OFFICE = "Office"
    OTHER = "Other"


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address_type = Column(Enum(AddressType), nullable=False)
    address = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    phone1 = Column(String, nullable=True)
    phone2 = Column(String, nullable=True)
    fax = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    policies = relationship("Policy", back_populates="client", cascade="all, delete-orphan")
