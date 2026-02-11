from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Clause(Base):
    __tablename__ = "clauses"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    clause_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    clause_limit = Column(Numeric(15, 2), nullable=True)
    remarks = Column(Text, nullable=True)
    is_checked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    policy = relationship("Policy", back_populates="clauses")


# Default clauses to seed
DEFAULT_CLAUSES = [
    "Tariff Endorsements",
    "Terrorism Clause",
    "Hypothecation Clause",
    "No Known Loss Clause",
    "Windscreen Breakage Clause",
    "Personal Accident Clause",
    "Third Party Liability Clause",
]
