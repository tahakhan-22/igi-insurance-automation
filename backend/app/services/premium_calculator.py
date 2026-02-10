"""
Premium calculation service
All business logic for premium calculations lives here
"""
from decimal import Decimal
from typing import Dict
from sqlalchemy.orm import Session
from app.models.peril_calculation import PerilCalculation, CalculationBasis
from app.models.item_detail import ItemDetail
from app.models.discount import Discount, PolicyDiscount
from app.models.product_setup import ProductSetup
from app.models.policy import Policy


def calculate_peril_premium(
    base_value: Decimal,
    rate_percent: Decimal,
    percent_of_rate: Decimal,
    calculation_basis: CalculationBasis,
    flat_amount: Decimal
) -> Decimal:
    """
    Calculate peril premium based on calculation basis
    
    Args:
        base_value: Base value for calculation
        rate_percent: Rate percentage
        percent_of_rate: Percent of rate to apply (default 100)
        calculation_basis: Type of calculation (percentage, flat, per_mille)
        flat_amount: Flat amount if basis is flat
        
    Returns:
        Calculated premium as Decimal
    """
    if calculation_basis == CalculationBasis.FLAT:
        return flat_amount
    elif calculation_basis == CalculationBasis.PERCENTAGE:
        return (base_value * (rate_percent / Decimal("100")) * (percent_of_rate / Decimal("100")))
    elif calculation_basis == CalculationBasis.PER_MILLE:
        return (base_value * (rate_percent / Decimal("1000")) * (percent_of_rate / Decimal("100")))
    else:
        return Decimal("0.00")


def calculate_item_basic_premium(db: Session, item_id: int) -> Decimal:
    """
    Calculate total basic premium for an item by summing all peril premiums
    
    Args:
        db: Database session
        item_id: Item detail ID
        
    Returns:
        Total basic premium
    """
    perils = db.query(PerilCalculation).filter(PerilCalculation.item_id == item_id).all()
    total = Decimal("0.00")
    
    for peril in perils:
        premium = calculate_peril_premium(
            peril.base_value,
            peril.rate_percent,
            peril.percent_of_rate,
            peril.calculation_basis,
            peril.flat_amount
        )
        # Update peril's basic_premium
        peril.basic_premium = premium
        total += premium
    
    db.commit()
    return total


def calculate_item_discounts(db: Session, item_id: int) -> Decimal:
    """
    Calculate total discount amount for an item
    Each discount: sum_insured * rate_percent / 100
    
    Args:
        db: Database session
        item_id: Item detail ID
        
    Returns:
        Total discount amount
    """
    item = db.query(ItemDetail).filter(ItemDetail.id == item_id).first()
    if not item:
        return Decimal("0.00")
    
    discounts = db.query(Discount).filter(Discount.item_id == item_id).all()
    total = Decimal("0.00")
    
    for discount in discounts:
        discount_amount = item.sum_insured * (discount.rate_percent / Decimal("100"))
        discount.amount = discount_amount
        total += discount_amount
    
    db.commit()
    return total


def calculate_charges(db: Session, policy_id: int) -> Dict[str, Decimal]:
    """
    Calculate charges based on ProductSetup flags
    
    Args:
        db: Database session
        policy_id: Policy ID
        
    Returns:
        Dict with charge names and amounts
    """
    product_setup = db.query(ProductSetup).filter(ProductSetup.policy_id == policy_id).first()
    if not product_setup:
        return {}
    
    # Get policy to access basic premium
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        return {}
    
    # Calculate basic premium first
    items = db.query(ItemDetail).filter(ItemDetail.policy_id == policy_id).all()
    basic_premium = sum(item.basic_premium for item in items)
    
    charges = {}
    
    if product_setup.admin_sub_charges:
        charges["admin_sub_charges"] = basic_premium * Decimal("0.05")  # 5%
    
    if product_setup.sales_tax_fed:
        charges["sales_tax_fed"] = basic_premium * Decimal("0.13")  # 13% FED
    
    if product_setup.federal_insurance_fee:
        charges["federal_insurance_fee"] = Decimal("500.00")  # Flat 500 PKR
    
    if product_setup.stamp_duty:
        charges["stamp_duty"] = Decimal("200.00")  # Flat 200 PKR
    
    return charges


def calculate_gross_premium(db: Session, policy_id: int) -> Decimal:
    """
    Calculate gross premium: sum of all item basic premiums + charges
    
    Args:
        db: Database session
        policy_id: Policy ID
        
    Returns:
        Gross premium
    """
    # Sum all item basic premiums
    items = db.query(ItemDetail).filter(ItemDetail.policy_id == policy_id).all()
    basic_premium = sum(item.basic_premium for item in items)
    
    # Add charges
    charges = calculate_charges(db, policy_id)
    total_charges = sum(charges.values())
    
    return basic_premium + total_charges


def calculate_net_premium(db: Session, policy_id: int) -> Decimal:
    """
    Calculate net premium: gross_premium - sum(policy_discounts) - sum(item_discounts)
    
    Args:
        db: Database session
        policy_id: Policy ID
        
    Returns:
        Net premium
    """
    gross_premium = calculate_gross_premium(db, policy_id)
    
    # Sum policy-level discounts
    policy_discounts = db.query(PolicyDiscount).filter(PolicyDiscount.policy_id == policy_id).all()
    total_policy_discount = sum(discount.amount for discount in policy_discounts)
    
    # Sum item-level discounts
    items = db.query(ItemDetail).filter(ItemDetail.policy_id == policy_id).all()
    total_item_discount = Decimal("0.00")
    for item in items:
        total_item_discount += calculate_item_discounts(db, item.id)
    
    return gross_premium - total_policy_discount - total_item_discount


def recalculate_policy(db: Session, policy_id: int) -> None:
    """
    Master function: recalculates everything and updates policy record
    
    Args:
        db: Database session
        policy_id: Policy ID
    """
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        return
    
    # Recalculate each item's basic premium
    items = db.query(ItemDetail).filter(ItemDetail.policy_id == policy_id).all()
    for item in items:
        basic_premium = calculate_item_basic_premium(db, item.id)
        item.basic_premium = basic_premium
        item.gross_premium = basic_premium  # Before discounts
    
    # Calculate sum insured
    total_sum_insured = sum(item.sum_insured for item in items)
    
    # Calculate gross and net premium
    gross = calculate_gross_premium(db, policy_id)
    net = calculate_net_premium(db, policy_id)
    
    # Update policy
    policy.sum_insured = total_sum_insured
    policy.gross_premium = gross
    policy.net_premium = net
    policy.premium_payable = net  # For now, premium_payable = net_premium
    
    db.commit()
