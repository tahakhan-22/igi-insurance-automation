from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Agency(Base):
    __tablename__ = "agencies"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    agent_name = Column(String, nullable=False)
    apportionment_percent = Column(Numeric(10, 4), default=0)
    amount = Column(Numeric(15, 2), default=0)
    premium_share_percent = Column(Numeric(10, 4), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    policy = relationship("Policy", back_populates="agencies")
