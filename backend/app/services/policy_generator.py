"""
Policy document generator service
Aggregates all policy data for template rendering
"""
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.policy import Policy
from app.models.client import Client
from app.models.item_detail import ItemDetail
from app.models.vehicle import Vehicle
from app.models.peril_calculation import PerilCalculation
from app.models.clause import Clause
from app.models.warranty import Warranty
from app.models.deductible import Deductible
from app.models.agency import Agency
from app.models.document_description import DocumentDescription
from app.services.premium_calculator import calculate_charges
from app.services.computational_sheet import generate_computational_sheet


def generate_final_policy(db: Session, policy_id: int) -> Dict[str, Any]:
    """
    Aggregate ALL data from all modules into final policy structure
    No manual entry — everything auto-populated from database
    
    Args:
        db: Database session
        policy_id: Policy ID
        
    Returns:
        Complete policy dict for template rendering
    """
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        return {}
    
    # Get client data
    client = db.query(Client).filter(Client.id == policy.client_id).first()
    client_data = {
        "name": client.name,
        "address_type": client.address_type.value if client.address_type else None,
        "address": client.address,
        "country": client.country,
        "city": client.city,
        "phone1": client.phone1,
        "phone2": client.phone2,
        "fax": client.fax,
        "email": client.email
    } if client else {}
    
    # Get vehicle schedule
    vehicles = db.query(Vehicle).filter(Vehicle.policy_id == policy_id).all()
    vehicle_schedule = [
        {
            "registration_status": vehicle.registration_status.value if vehicle.registration_status else None,
            "registration_no": vehicle.registration_no,
            "engine_no": vehicle.engine_no,
            "chassis_no": vehicle.chassis_no,
            "make": vehicle.make,
            "model": vehicle.model,
            "year": vehicle.year_of_manufacturing,
            "age": vehicle.vehicle_age,
            "color": vehicle.color,
            "body_type": vehicle.body_type,
            "engine_cc": vehicle.engine_cc,
            "passengers": vehicle.passengers,
            "accessories_sum_insured": float(vehicle.accessories_sum_insured) if vehicle.accessories_sum_insured else 0
        }
        for vehicle in vehicles
    ]
    
    # Get perils coverage
    items = db.query(ItemDetail).filter(ItemDetail.policy_id == policy_id).all()
    perils_coverage = []
    for item in items:
        perils = db.query(PerilCalculation).filter(PerilCalculation.item_id == item.id).all()
        for peril in perils:
            perils_coverage.append({
                "item_no": item.item_no,
                "peril_type": peril.peril_type,
                "base_value": float(peril.base_value),
                "rate": float(peril.rate_percent),
                "premium": float(peril.basic_premium)
            })
    
    # Get charges
    charges_dict = calculate_charges(db, policy_id)
    charges_breakdown = [
        {"name": name.replace("_", " ").title(), "amount": float(amount)}
        for name, amount in charges_dict.items()
    ]
    
    # Get discounts
    comp_sheet = generate_computational_sheet(db, policy_id)
    discounts_applied = comp_sheet.get("item_discounts", []) + comp_sheet.get("policy_discounts", [])
    
    # Premium summary
    premium_summary = {
        "basic_premium": float(comp_sheet.get("total_basic_premium", 0)),
        "charges": float(comp_sheet.get("total_charges", 0)),
        "gross_premium": float(comp_sheet.get("gross_premium", 0)),
        "discounts": float(comp_sheet.get("total_discounts", 0)),
        "net_premium": float(comp_sheet.get("net_premium", 0)),
        "premium_payable": float(policy.premium_payable)
    }
    
    # Get endorsement clauses
    clauses = db.query(Clause).filter(Clause.policy_id == policy_id, Clause.is_checked == True).all()
    endorsement_clauses = [
        {
            "name": clause.clause_name,
            "description": clause.description,
            "limit": float(clause.clause_limit) if clause.clause_limit else None,
            "remarks": clause.remarks
        }
        for clause in clauses
    ]
    
    # Get warranties
    warranties = db.query(Warranty).filter(Warranty.policy_id == policy_id, Warranty.is_active == True).all()
    warranties_list = [
        {
            "type": warranty.warranty_type,
            "details": warranty.details
        }
        for warranty in warranties
    ]
    
    # Get deductibles
    deductibles = db.query(Deductible).filter(Deductible.policy_id == policy_id).all()
    deductibles_list = [
        {
            "type": deductible.deductible_type,
            "amount": float(deductible.amount),
            "conditions": deductible.conditions
        }
        for deductible in deductibles
    ]
    
    # Get agency details
    agencies = db.query(Agency).filter(Agency.policy_id == policy_id).all()
    agency_details = [
        {
            "agent_name": agency.agent_name,
            "apportionment_percent": float(agency.apportionment_percent),
            "amount": float(agency.amount),
            "premium_share_percent": float(agency.premium_share_percent)
        }
        for agency in agencies
    ]
    
    # Get terms and conditions
    doc_desc = db.query(DocumentDescription).filter(DocumentDescription.policy_id == policy_id).first()
    terms_conditions = doc_desc.terms_conditions if doc_desc else "Standard terms and conditions apply."
    
    return {
        "policy_data": {
            "policy_number": policy.policy_number,
            "policy_type": policy.policy_type,
            "region": policy.region,
            "currency": policy.currency,
            "start_date": policy.start_date.isoformat() if policy.start_date else None,
            "end_date": policy.end_date.isoformat() if policy.end_date else None,
            "status": policy.status.value if policy.status else None,
            "sum_insured": float(policy.sum_insured),
            "cnic_ntn": policy.cnic_ntn,
            "claim_limit": float(policy.claim_limit) if policy.claim_limit else None,
            "industry": policy.industry,
            "notes": policy.notes
        },
        "client_data": client_data,
        "vehicle_schedule": vehicle_schedule,
        "perils_coverage": perils_coverage,
        "charges_breakdown": charges_breakdown,
        "discounts_applied": discounts_applied,
        "premium_summary": premium_summary,
        "endorsement_clauses": endorsement_clauses,
        "warranties": warranties_list,
        "deductibles": deductibles_list,
        "agency_details": agency_details,
        "terms_conditions": terms_conditions
    }


def generate_cover_letter(db: Session, policy_id: int) -> str:
    """
    Render cover letter HTML template with policy data
    
    Args:
        db: Database session
        policy_id: Policy ID
        
    Returns:
        HTML string
    """
    from jinja2 import Environment, FileSystemLoader
    import os
    
    template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("cover_letter.html")
    
    policy_data = generate_final_policy(db, policy_id)
    
    return template.render(**policy_data)


def generate_policy_document(db: Session, policy_id: int) -> str:
    """
    Render policy document HTML template with all data
    
    Args:
        db: Database session
        policy_id: Policy ID
        
    Returns:
        HTML string
    """
    from jinja2 import Environment, FileSystemLoader
    import os
    
    template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("policy_document.html")
    
    policy_data = generate_final_policy(db, policy_id)
    
    return template.render(**policy_data)
