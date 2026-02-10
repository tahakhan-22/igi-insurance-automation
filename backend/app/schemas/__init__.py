# Import all schemas
from app.schemas.client import ClientBase, ClientCreate, ClientUpdate, Client
from app.schemas.policy import PolicyBase, PolicyCreate, PolicyUpdate, Policy
from app.schemas.bank import BankBase, BankCreate, BankUpdate, Bank
from app.schemas.product_setup import ProductSetupBase, ProductSetupCreate, ProductSetupUpdate, ProductSetup
from app.schemas.item_detail import ItemDetailBase, ItemDetailCreate, ItemDetailUpdate, ItemDetail
from app.schemas.peril_calculation import PerilCalculationBase, PerilCalculationCreate, PerilCalculationUpdate, PerilCalculation
from app.schemas.vehicle import VehicleBase, VehicleCreate, VehicleUpdate, Vehicle
from app.schemas.discount import DiscountBase, DiscountCreate, DiscountUpdate, Discount, PolicyDiscountBase, PolicyDiscountCreate, PolicyDiscountUpdate, PolicyDiscount
from app.schemas.deductible import DeductibleBase, DeductibleCreate, DeductibleUpdate, Deductible
from app.schemas.clause import ClauseBase, ClauseCreate, ClauseUpdate, Clause
from app.schemas.warranty import WarrantyBase, WarrantyCreate, WarrantyUpdate, Warranty
from app.schemas.agency import AgencyBase, AgencyCreate, AgencyUpdate, Agency

__all__ = [
    "ClientBase", "ClientCreate", "ClientUpdate", "Client",
    "PolicyBase", "PolicyCreate", "PolicyUpdate", "Policy",
    "BankBase", "BankCreate", "BankUpdate", "Bank",
    "ProductSetupBase", "ProductSetupCreate", "ProductSetupUpdate", "ProductSetup",
    "ItemDetailBase", "ItemDetailCreate", "ItemDetailUpdate", "ItemDetail",
    "PerilCalculationBase", "PerilCalculationCreate", "PerilCalculationUpdate", "PerilCalculation",
    "VehicleBase", "VehicleCreate", "VehicleUpdate", "Vehicle",
    "DiscountBase", "DiscountCreate", "DiscountUpdate", "Discount",
    "PolicyDiscountBase", "PolicyDiscountCreate", "PolicyDiscountUpdate", "PolicyDiscount",
    "DeductibleBase", "DeductibleCreate", "DeductibleUpdate", "Deductible",
    "ClauseBase", "ClauseCreate", "ClauseUpdate", "Clause",
    "WarrantyBase", "WarrantyCreate", "WarrantyUpdate", "Warranty",
    "AgencyBase", "AgencyCreate", "AgencyUpdate", "Agency",
]
