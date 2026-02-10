from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class BankBase(BaseModel):
    serial_no: Optional[int] = None
    bank_type: Optional[str] = None
    limits: Optional[Decimal] = Field(default=None, ge=0)


class BankCreate(BankBase):
    policy_id: int


class BankUpdate(BaseModel):
    serial_no: Optional[int] = None
    bank_type: Optional[str] = None
    limits: Optional[Decimal] = None


class Bank(BankBase):
    id: int
    policy_id: int
    created_at: datetime

    class Config:
        from_attributes = True
