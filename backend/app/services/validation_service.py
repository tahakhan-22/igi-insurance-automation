"""
Validation service
All validation logic for emails, phones, duplicates, etc.
"""
import re
from typing import Tuple, List, Optional
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.models.agency import Agency
from decimal import Decimal


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format (Pakistani format)
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not phone:
        return False
    
    # Pakistani phone format: +923001234567 or 03001234567
    phone_pattern = r'^(\+92|0)?3[0-9]{9}$'
    return bool(re.match(phone_pattern, phone.replace(" ", "").replace("-", "")))


def check_engine_duplicate(db: Session, engine_no: str, exclude_vehicle_id: Optional[int] = None) -> bool:
    """
    Check if engine number already exists in database
    
    Args:
        db: Database session
        engine_no: Engine number to check
        exclude_vehicle_id: Vehicle ID to exclude from check (for updates)
        
    Returns:
        True if duplicate found, False otherwise
    """
    if not engine_no:
        return False
    
    query = db.query(Vehicle).filter(Vehicle.engine_no == engine_no)
    
    if exclude_vehicle_id:
        query = query.filter(Vehicle.id != exclude_vehicle_id)
    
    return query.first() is not None


def check_chassis_duplicate(db: Session, chassis_no: str, exclude_vehicle_id: Optional[int] = None) -> bool:
    """
    Check if chassis number already exists in database
    
    Args:
        db: Database session
        chassis_no: Chassis number to check
        exclude_vehicle_id: Vehicle ID to exclude from check (for updates)
        
    Returns:
        True if duplicate found, False otherwise
    """
    if not chassis_no:
        return False
    
    query = db.query(Vehicle).filter(Vehicle.chassis_no == chassis_no)
    
    if exclude_vehicle_id:
        query = query.filter(Vehicle.id != exclude_vehicle_id)
    
    return query.first() is not None


def validate_agency_apportionment(db: Session, policy_id: int) -> Tuple[bool, str]:
    """
    Validate that agency apportionment sums to 100%
    
    Args:
        db: Database session
        policy_id: Policy ID
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    agencies = db.query(Agency).filter(Agency.policy_id == policy_id).all()
    
    if not agencies:
        return True, ""
    
    total_apportionment = sum(agency.apportionment_percent for agency in agencies)
    
    if total_apportionment != Decimal("100.00"):
        return False, f"Agency apportionment must sum to 100%. Current total: {total_apportionment}%"
    
    return True, ""


def calculate_vehicle_age(year_of_manufacturing: int) -> int:
    """
    Calculate vehicle age from manufacturing year
    
    Args:
        year_of_manufacturing: Year vehicle was manufactured
        
    Returns:
        Vehicle age in years
    """
    from datetime import datetime
    current_year = datetime.now().year
    return current_year - year_of_manufacturing


def validate_required_fields(data: dict, required: List[str]) -> List[str]:
    """
    Validate that required fields are present and not empty
    
    Args:
        data: Data dictionary to validate
        required: List of required field names
        
    Returns:
        List of missing field names
    """
    missing = []
    
    for field in required:
        if field not in data or data[field] is None or data[field] == "":
            missing.append(field)
    
    return missing
