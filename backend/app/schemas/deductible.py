from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class DeductibleBase(BaseModel):
    deductible_type: str
    amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    conditions: Optional[str] = None


class DeductibleCreate(DeductibleBase):
    policy_id: int


class DeductibleUpdate(BaseModel):
    deductible_type: Optional[str] = None
    amount: Optional[Decimal] = None
    conditions: Optional[str] = None


class Deductible(DeductibleBase):
    id: int
    policy_id: int
    created_at: datetime

    class Config:
        from_attributes = True
