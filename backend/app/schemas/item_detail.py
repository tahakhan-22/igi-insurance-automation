from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ItemDetailBase(BaseModel):
    schedule_id: Optional[str] = None
    item_no: Optional[int] = None
    sum_insured: Decimal = Field(default=Decimal("0.00"), ge=0)
    basic_premium: Decimal = Field(default=Decimal("0.00"), ge=0)
    gross_premium: Decimal = Field(default=Decimal("0.00"), ge=0)
    risk_peril_reference: Optional[str] = None


class ItemDetailCreate(ItemDetailBase):
    policy_id: int


class ItemDetailUpdate(BaseModel):
    schedule_id: Optional[str] = None
    item_no: Optional[int] = None
    sum_insured: Optional[Decimal] = None
    basic_premium: Optional[Decimal] = None
    gross_premium: Optional[Decimal] = None
    risk_peril_reference: Optional[str] = None


class ItemDetail(ItemDetailBase):
    id: int
    policy_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
