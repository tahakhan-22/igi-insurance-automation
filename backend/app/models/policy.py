from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Date, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum
from datetime import datetime


class PolicyStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class Policy(Base):
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_number = Column(String, unique=True, nullable=False, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    policy_type = Column(String, nullable=True)
    region = Column(String, nullable=True)
    currency = Column(String, default="PKR")
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(Enum(PolicyStatus), default=PolicyStatus.DRAFT)
    sum_insured = Column(Numeric(15, 2), default=0)
    gross_premium = Column(Numeric(15, 2), default=0)
    net_premium = Column(Numeric(15, 2), default=0)
    premium_payable = Column(Numeric(15, 2), default=0)
    cnic_ntn = Column(String, nullable=True)
    claim_limit = Column(Numeric(15, 2), nullable=True)
    industry = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    client = relationship("Client", back_populates="policies")
    banks = relationship("Bank", back_populates="policy", cascade="all, delete-orphan")
    document_descriptions = relationship("DocumentDescription", back_populates="policy", cascade="all, delete-orphan")
    product_setups = relationship("ProductSetup", back_populates="policy", cascade="all, delete-orphan")
    items = relationship("ItemDetail", back_populates="policy", cascade="all, delete-orphan")
    vehicles = relationship("Vehicle", back_populates="policy", cascade="all, delete-orphan")
    deductibles = relationship("Deductible", back_populates="policy", cascade="all, delete-orphan")
    policy_discounts = relationship("PolicyDiscount", back_populates="policy", cascade="all, delete-orphan")
    clauses = relationship("Clause", back_populates="policy", cascade="all, delete-orphan")
    warranties = relationship("Warranty", back_populates="policy", cascade="all, delete-orphan")
    agencies = relationship("Agency", back_populates="policy", cascade="all, delete-orphan")


def generate_policy_number() -> str:
    """Generate unique policy number: IGI-MOT-YYYYMMDD-XXXX"""
    from datetime import datetime
    date_str = datetime.now().strftime("%Y%m%d")
    # In production, add sequential counter
    import random
    counter = random.randint(1000, 9999)
    return f"IGI-MOT-{date_str}-{counter}"
