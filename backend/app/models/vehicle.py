from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum
from datetime import datetime


class RegistrationStatus(str, enum.Enum):
    REGISTERED = "registered"
    UNREGISTERED = "unregistered"


class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item_details.id"), nullable=True)
    
    registration_status = Column(Enum(RegistrationStatus), default=RegistrationStatus.REGISTERED)
    registration_no = Column(String, nullable=True)
    engine_no = Column(String, nullable=True, index=True)
    chassis_no = Column(String, nullable=True, index=True)
    make = Column(String, nullable=True)
    model = Column(String, nullable=True)
    passengers = Column(Integer, nullable=True)
    body_type = Column(String, nullable=True)
    engine_cc = Column(Integer, nullable=True)
    year_of_manufacturing = Column(Integer, nullable=True)
    vehicle_age = Column(Integer, nullable=True)
    color = Column(String, nullable=True)
    accessories_sum_insured = Column(Numeric(15, 2), default=0)
    cnic = Column(String, nullable=True)
    license_no = Column(String, nullable=True)
    loan_po_no = Column(String, nullable=True)
    contact_details = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    policy = relationship("Policy", back_populates="vehicles")
    item = relationship("ItemDetail", back_populates="vehicles")


def calculate_vehicle_age(year_of_manufacturing: int) -> int:
    """Calculate vehicle age from manufacturing year"""
    current_year = datetime.now().year
    return current_year - year_of_manufacturing
