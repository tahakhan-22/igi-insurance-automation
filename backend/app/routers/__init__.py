# Routers package
# Import routers from their respective modules for easy access

from app.routers.clients import router as clients_router
from app.routers.policies import router as policies_router
from app.routers.banks import banks, product_setup, items, perils
from app.routers.vehicles import vehicles, discounts, policy_discounts, deductibles, clauses, warranties, agencies
from app.routers.final_policy import computational_sheet, final_policy, reminders, gmail_integration

__all__ = [
    "clients_router", "policies_router", 
    "banks", "product_setup", "items", "perils", 
    "vehicles", "discounts", "policy_discounts", "deductibles", "clauses", "warranties", "agencies",
    "computational_sheet", "final_policy", "reminders", "gmail_integration"
]
