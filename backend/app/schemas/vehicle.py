from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.vehicle import RegistrationStatus


class VehicleBase(BaseModel):
    registration_status: RegistrationStatus = RegistrationStatus.REGISTERED
    registration_no: Optional[str] = None
    engine_no: Optional[str] = None
    chassis_no: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    passengers: Optional[int] = None
    body_type: Optional[str] = None
    engine_cc: Optional[int] = None
    year_of_manufacturing: Optional[int] = None
    vehicle_age: Optional[int] = None
    color: Optional[str] = None
    accessories_sum_insured: Decimal = Field(default=Decimal("0.00"), ge=0)
    cnic: Optional[str] = None
    license_no: Optional[str] = None
    loan_po_no: Optional[str] = None
    contact_details: Optional[str] = None


class VehicleCreate(VehicleBase):
    policy_id: int
    item_id: Optional[int] = None


class VehicleUpdate(BaseModel):
    registration_status: Optional[RegistrationStatus] = None
    registration_no: Optional[str] = None
    engine_no: Optional[str] = None
    chassis_no: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    passengers: Optional[int] = None
    body_type: Optional[str] = None
    engine_cc: Optional[int] = None
    year_of_manufacturing: Optional[int] = None
    vehicle_age: Optional[int] = None
    color: Optional[str] = None
    accessories_sum_insured: Optional[Decimal] = None
    cnic: Optional[str] = None
    license_no: Optional[str] = None
    loan_po_no: Optional[str] = None
    contact_details: Optional[str] = None
    item_id: Optional[int] = None


class Vehicle(VehicleBase):
    id: int
    policy_id: int
    item_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
