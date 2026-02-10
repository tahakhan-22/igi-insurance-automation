"""
Computational sheet service
Generates read-only aggregation of all policy data
"""
from decimal import Decimal
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.policy import Policy
from app.models.item_detail import ItemDetail
from app.models.peril_calculation import PerilCalculation
from app.models.discount import Discount, PolicyDiscount
from app.models.clause import Clause
from app.models.warranty import Warranty
from app.services.premium_calculator import calculate_charges


def generate_computational_sheet(db: Session, policy_id: int) -> Dict[str, Any]:
    """
    Generate read-only computational sheet with all aggregated data
    
    Args:
        db: Database session
        policy_id: Policy ID
        
    Returns:
        Dictionary with all computational data
    """
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        return {}
    
    # Get all items
    items = db.query(ItemDetail).filter(ItemDetail.policy_id == policy_id).all()
    
    # Calculate charges
    charges_dict = calculate_charges(db, policy_id)
    charges = [{"name": name, "amount": float(amount)} for name, amount in charges_dict.items()]
    total_charges = sum(charges_dict.values())
    
    # Get clauses
    clauses_db = db.query(Clause).filter(Clause.policy_id == policy_id, Clause.is_checked == True).all()
    clauses = [
        {
            "name": clause.clause_name,
            "limit": float(clause.clause_limit) if clause.clause_limit else None,
            "description": clause.description
        }
        for clause in clauses_db
    ]
    
    # Get warranties
    warranties_db = db.query(Warranty).filter(Warranty.policy_id == policy_id, Warranty.is_active == True).all()
    warranties = [
        {
            "type": warranty.warranty_type,
            "details": warranty.details
        }
        for warranty in warranties_db
    ]
    
    # Get item discounts
    item_discounts = []
    total_item_discount = Decimal("0.00")
    for item in items:
        discounts = db.query(Discount).filter(Discount.item_id == item.id).all()
        for discount in discounts:
            item_discounts.append({
                "item_no": item.item_no,
                "discount_type": discount.discount_type,
                "rate_percent": float(discount.rate_percent),
                "amount": float(discount.amount)
            })
            total_item_discount += discount.amount
    
    # Get policy discounts
    policy_discounts_db = db.query(PolicyDiscount).filter(PolicyDiscount.policy_id == policy_id).all()
    policy_discounts = [
        {
            "type": discount.discount_type,
            "rate_percent": float(discount.rate_percent),
            "amount": float(discount.amount)
        }
        for discount in policy_discounts_db
    ]
    total_policy_discount = sum(d.amount for d in policy_discounts_db)
    
    # Get perils
    perils = []
    total_basic_premium = Decimal("0.00")
    for item in items:
        perils_db = db.query(PerilCalculation).filter(PerilCalculation.item_id == item.id).all()
        for peril in perils_db:
            perils.append({
                "item_no": item.item_no,
                "peril_type": peril.peril_type,
                "base_value": float(peril.base_value),
                "rate_percent": float(peril.rate_percent),
                "premium": float(peril.basic_premium)
            })
            total_basic_premium += peril.basic_premium
    
    # Calculate totals
    total_sum_insured = sum(item.sum_insured for item in items)
    total_discounts = total_item_discount + total_policy_discount
    gross_premium = total_basic_premium + total_charges
    net_premium = gross_premium - total_discounts
    
    return {
        "charges": charges,
        "clauses": clauses,
        "warranties": warranties,
        "item_discounts": item_discounts,
        "policy_discounts": policy_discounts,
        "perils": perils,
        "total_basic_premium": float(total_basic_premium),
        "total_charges": float(total_charges),
        "gross_premium": float(gross_premium),
        "total_discounts": float(total_discounts),
        "net_premium": float(net_premium),
        "sum_insured": float(total_sum_insured)
    }
