from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductSetupBase(BaseModel):
    # Peril flags
    legal_liability: bool = False
    accident_passengers: bool = False
    insured_estimated_value: bool = False
    rsd_md_terrorism: bool = False
    basic_premium_flag: bool = False
    pa_to_insured: bool = False
    
    # Charge flags
    admin_sub_charges: bool = False
    sales_tax_fed: bool = False
    federal_insurance_fee: bool = False
    stamp_duty: bool = False


class ProductSetupCreate(ProductSetupBase):
    policy_id: int


class ProductSetupUpdate(ProductSetupBase):
    pass


class ProductSetup(ProductSetupBase):
    id: int
    policy_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
