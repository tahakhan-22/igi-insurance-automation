from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ProductSetup(Base):
    __tablename__ = "product_setups"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    
    # Peril flags
    legal_liability = Column(Boolean, default=False)
    accident_passengers = Column(Boolean, default=False)
    insured_estimated_value = Column(Boolean, default=False)
    rsd_md_terrorism = Column(Boolean, default=False)
    basic_premium_flag = Column(Boolean, default=False)
    pa_to_insured = Column(Boolean, default=False)
    
    # Charge flags
    admin_sub_charges = Column(Boolean, default=False)
    sales_tax_fed = Column(Boolean, default=False)
    federal_insurance_fee = Column(Boolean, default=False)
    stamp_duty = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    policy = relationship("Policy", back_populates="product_setups")
