from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WarrantyBase(BaseModel):
    warranty_type: str
    details: Optional[str] = None
    is_active: bool = True


class WarrantyCreate(WarrantyBase):
    policy_id: int


class WarrantyUpdate(BaseModel):
    warranty_type: Optional[str] = None
    details: Optional[str] = None
    is_active: Optional[bool] = None


class Warranty(WarrantyBase):
    id: int
    policy_id: int
    created_at: datetime

    class Config:
        from_attributes = True
