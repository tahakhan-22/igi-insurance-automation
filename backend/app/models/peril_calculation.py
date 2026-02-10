from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class CalculationBasis(str, enum.Enum):
    PERCENTAGE = "percentage"
    FLAT = "flat"
    PER_MILLE = "per_mille"


class PerilCalculation(Base):
    __tablename__ = "peril_calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("item_details.id"), nullable=False)
    peril_type = Column(String, nullable=False)
    base_value = Column(Numeric(15, 2), default=0)
    rate_percent = Column(Numeric(10, 4), default=0)
    percent_of_rate = Column(Numeric(10, 4), default=100)
    calculation_basis = Column(Enum(CalculationBasis), default=CalculationBasis.PERCENTAGE)
    flat_amount = Column(Numeric(15, 2), default=0)
    basic_premium = Column(Numeric(15, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    item = relationship("ItemDetail", back_populates="perils")
