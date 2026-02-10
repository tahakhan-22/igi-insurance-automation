from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class DiscountBase(BaseModel):
    discount_type: str
    rate_percent: Decimal = Field(default=Decimal("0.0000"), ge=0)
    amount: Decimal = Field(default=Decimal("0.00"), ge=0)


class DiscountCreate(DiscountBase):
    item_id: int


class DiscountUpdate(BaseModel):
    discount_type: Optional[str] = None
    rate_percent: Optional[Decimal] = None
    amount: Optional[Decimal] = None


class Discount(DiscountBase):
    id: int
    item_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PolicyDiscountBase(BaseModel):
    discount_type: str
    rate_percent: Decimal = Field(default=Decimal("0.0000"), ge=0)
    amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    unique_identifier: Optional[str] = None


class PolicyDiscountCreate(PolicyDiscountBase):
    policy_id: int


class PolicyDiscountUpdate(BaseModel):
    discount_type: Optional[str] = None
    rate_percent: Optional[Decimal] = None
    amount: Optional[Decimal] = None


class PolicyDiscount(PolicyDiscountBase):
    id: int
    policy_id: int
    created_at: datetime

    class Config:
        from_attributes = True
