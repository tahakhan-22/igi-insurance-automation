from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class AgencyBase(BaseModel):
    agent_name: str
    apportionment_percent: Decimal = Field(default=Decimal("0.0000"), ge=0, le=100)
    amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    premium_share_percent: Decimal = Field(default=Decimal("0.0000"), ge=0, le=100)


class AgencyCreate(AgencyBase):
    policy_id: int


class AgencyUpdate(BaseModel):
    agent_name: Optional[str] = None
    apportionment_percent: Optional[Decimal] = None
    amount: Optional[Decimal] = None
    premium_share_percent: Optional[Decimal] = None


class Agency(AgencyBase):
    id: int
    policy_id: int
    created_at: datetime

    class Config:
        from_attributes = True
