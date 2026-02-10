from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from app.models.policy import PolicyStatus


class PolicyBase(BaseModel):
    client_id: int
    policy_type: Optional[str] = None
    region: Optional[str] = None
    currency: str = "PKR"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: PolicyStatus = PolicyStatus.DRAFT
    sum_insured: Decimal = Field(default=Decimal("0.00"), ge=0)
    gross_premium: Decimal = Field(default=Decimal("0.00"), ge=0)
    net_premium: Decimal = Field(default=Decimal("0.00"), ge=0)
    premium_payable: Decimal = Field(default=Decimal("0.00"), ge=0)
    cnic_ntn: Optional[str] = None
    claim_limit: Optional[Decimal] = None
    industry: Optional[str] = None
    notes: Optional[str] = None


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(BaseModel):
    client_id: Optional[int] = None
    policy_type: Optional[str] = None
    region: Optional[str] = None
    currency: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[PolicyStatus] = None
    sum_insured: Optional[Decimal] = None
    gross_premium: Optional[Decimal] = None
    net_premium: Optional[Decimal] = None
    premium_payable: Optional[Decimal] = None
    cnic_ntn: Optional[str] = None
    claim_limit: Optional[Decimal] = None
    industry: Optional[str] = None
    notes: Optional[str] = None


class Policy(PolicyBase):
    id: int
    policy_number: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
