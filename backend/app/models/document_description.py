from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class DocumentDescription(Base):
    __tablename__ = "document_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    description_text = Column(Text, nullable=True)
    terms_conditions = Column(Text, nullable=True)
    vehicle_inspection_notes = Column(Text, nullable=True)
    showroom_delivery_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    policy = relationship("Policy", back_populates="document_descriptions")
