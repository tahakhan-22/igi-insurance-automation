from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ClauseBase(BaseModel):
    clause_name: str
    description: Optional[str] = None
    clause_limit: Optional[Decimal] = Field(default=None, ge=0)
    remarks: Optional[str] = None
    is_checked: bool = False


class ClauseCreate(ClauseBase):
    policy_id: int


class ClauseUpdate(BaseModel):
    clause_name: Optional[str] = None
    description: Optional[str] = None
    clause_limit: Optional[Decimal] = None
    remarks: Optional[str] = None
    is_checked: Optional[bool] = None


class Clause(ClauseBase):
    id: int
    policy_id: int
    created_at: datetime

    class Config:
        from_attributes = True
