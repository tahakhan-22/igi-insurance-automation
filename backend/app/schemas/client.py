from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.client import AddressType


class ClientBase(BaseModel):
    name: str
    address_type: AddressType
    address: str
    country: str
    city: str
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[EmailStr] = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    address_type: Optional[AddressType] = None
    address: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[EmailStr] = None


class Client(ClientBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
