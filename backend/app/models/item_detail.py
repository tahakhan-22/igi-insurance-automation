from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ItemDetail(Base):
    __tablename__ = "item_details"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    schedule_id = Column(String, nullable=True)
    item_no = Column(Integer, nullable=True)
    sum_insured = Column(Numeric(15, 2), default=0)
    basic_premium = Column(Numeric(15, 2), default=0)
    gross_premium = Column(Numeric(15, 2), default=0)
    risk_peril_reference = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    policy = relationship("Policy", back_populates="items")
    perils = relationship("PerilCalculation", back_populates="item", cascade="all, delete-orphan")
    discounts = relationship("Discount", back_populates="item", cascade="all, delete-orphan")
    vehicles = relationship("Vehicle", back_populates="item")
