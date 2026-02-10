from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Discount(Base):
    """Item-level discount"""
    __tablename__ = "discounts"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("item_details.id"), nullable=False)
    discount_type = Column(String, nullable=False)
    rate_percent = Column(Numeric(10, 4), default=0)
    amount = Column(Numeric(15, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    item = relationship("ItemDetail", back_populates="discounts")


class PolicyDiscount(Base):
    """Policy-level discount"""
    __tablename__ = "policy_discounts"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    unique_identifier = Column(String, unique=True, nullable=True)
    discount_type = Column(String, nullable=False)
    rate_percent = Column(Numeric(10, 4), default=0)
    amount = Column(Numeric(15, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    policy = relationship("Policy", back_populates="policy_discounts")
