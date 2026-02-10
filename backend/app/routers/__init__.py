# Import all routers
from app.routers import clients, policies, banks, product_setup, items, perils, vehicles
from app.routers import discounts, deductibles, clauses, warranties, agencies
from app.routers import computational_sheet, final_policy, reminders, gmail_integration

__all__ = [
    "clients", "policies", "banks", "product_setup", "items", "perils", "vehicles",
    "discounts", "deductibles", "clauses", "warranties", "agencies",
    "computational_sheet", "final_policy", "reminders", "gmail_integration"
]
