# Import all models for Alembic
from app.models.client import Client
from app.models.policy import Policy
from app.models.bank import Bank
from app.models.document_description import DocumentDescription
from app.models.product_setup import ProductSetup
from app.models.item_detail import ItemDetail
from app.models.peril_calculation import PerilCalculation
from app.models.vehicle import Vehicle
from app.models.discount import Discount, PolicyDiscount
from app.models.deductible import Deductible
from app.models.clause import Clause
from app.models.warranty import Warranty
from app.models.agency import Agency
from app.models.reminder import Reminder

__all__ = [
    "Client",
    "Policy",
    "Bank",
    "DocumentDescription",
    "ProductSetup",
    "ItemDetail",
    "PerilCalculation",
    "Vehicle",
    "Discount",
    "PolicyDiscount",
    "Deductible",
    "Clause",
    "Warranty",
    "Agency",
    "Reminder",
]
