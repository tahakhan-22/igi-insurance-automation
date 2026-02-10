from pydantic import BaseModel
from typing import Any, Dict


class FinalPolicy(BaseModel):
    """Complete policy document with all aggregated data"""
    policy_data: Dict[str, Any]
    client_data: Dict[str, Any]
    vehicle_schedule: list
    perils_coverage: list
    charges_breakdown: list
    discounts_applied: list
    premium_summary: Dict[str, Any]
    endorsement_clauses: list
    warranties: list
    deductibles: list
    agency_details: list
    terms_conditions: str
    
    class Config:
        from_attributes = True
