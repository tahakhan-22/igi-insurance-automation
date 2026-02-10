from pydantic import BaseModel
from typing import List, Dict, Any
from decimal import Decimal


class ComputationalSheet(BaseModel):
    """Read-only computational sheet aggregation"""
    charges: List[Dict[str, Any]]
    clauses: List[Dict[str, Any]]
    warranties: List[Dict[str, Any]]
    item_discounts: List[Dict[str, Any]]
    policy_discounts: List[Dict[str, Any]]
    perils: List[Dict[str, Any]]
    total_basic_premium: Decimal
    total_charges: Decimal
    gross_premium: Decimal
    total_discounts: Decimal
    net_premium: Decimal
    sum_insured: Decimal
    
    class Config:
        from_attributes = True
