from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.peril_calculation import CalculationBasis


class PerilCalculationBase(BaseModel):
    peril_type: str
    base_value: Decimal = Field(default=Decimal("0.00"), ge=0)
    rate_percent: Decimal = Field(default=Decimal("0.0000"), ge=0)
    percent_of_rate: Decimal = Field(default=Decimal("100.0000"), ge=0)
    calculation_basis: CalculationBasis = CalculationBasis.PERCENTAGE
    flat_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    basic_premium: Decimal = Field(default=Decimal("0.00"), ge=0)


class PerilCalculationCreate(PerilCalculationBase):
    item_id: int


class PerilCalculationUpdate(BaseModel):
    peril_type: Optional[str] = None
    base_value: Optional[Decimal] = None
    rate_percent: Optional[Decimal] = None
    percent_of_rate: Optional[Decimal] = None
    calculation_basis: Optional[CalculationBasis] = None
    flat_amount: Optional[Decimal] = None
    basic_premium: Optional[Decimal] = None


class PerilCalculation(PerilCalculationBase):
    id: int
    item_id: int
    created_at: datetime

    class Config:
        from_attributes = True
