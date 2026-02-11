"""
Vehicles, Discounts, Deductibles, Clauses, Warranties, Agencies routers
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.vehicle import Vehicle, calculate_vehicle_age
from app.models.discount import Discount, PolicyDiscount
from app.models.deductible import Deductible
from app.models.clause import Clause
from app.models.warranty import Warranty
from app.models.agency import Agency
from app.schemas.vehicle import Vehicle as VehicleSchema, VehicleCreate, VehicleUpdate
from app.schemas.discount import (Discount as DiscountSchema, DiscountCreate, DiscountUpdate,
                                   PolicyDiscount as PolicyDiscountSchema, PolicyDiscountCreate, PolicyDiscountUpdate)
from app.schemas.deductible import Deductible as DeductibleSchema, DeductibleCreate, DeductibleUpdate
from app.schemas.clause import Clause as ClauseSchema, ClauseCreate, ClauseUpdate
from app.schemas.warranty import Warranty as WarrantySchema, WarrantyCreate, WarrantyUpdate
from app.schemas.agency import Agency as AgencySchema, AgencyCreate, AgencyUpdate
from app.services.validation_service import check_engine_duplicate, check_chassis_duplicate, validate_agency_apportionment
from app.services.premium_calculator import recalculate_policy, calculate_item_discounts

# Vehicles Router
vehicles = APIRouter(prefix="/api/policies/{policy_id}/vehicles", tags=["vehicles"])

@vehicles.post("/", response_model=VehicleSchema)
def create_vehicle(policy_id: int, vehicle: VehicleCreate, db: Session = Depends(get_db)):
    # Check duplicates
    if vehicle.engine_no and check_engine_duplicate(db, vehicle.engine_no):
        raise HTTPException(status_code=400, detail="Engine number already exists")
    if vehicle.chassis_no and check_chassis_duplicate(db, vehicle.chassis_no):
        raise HTTPException(status_code=400, detail="Chassis number already exists")
    
    vehicle_data = vehicle.model_dump()
    vehicle_data["policy_id"] = policy_id
    
    # Calculate vehicle age
    if vehicle_data.get("year_of_manufacturing"):
        vehicle_data["vehicle_age"] = calculate_vehicle_age(vehicle_data["year_of_manufacturing"])
    
    db_vehicle = Vehicle(**vehicle_data)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@vehicles.get("/", response_model=List[VehicleSchema])
def list_vehicles(policy_id: int, db: Session = Depends(get_db)):
    return db.query(Vehicle).filter(Vehicle.policy_id == policy_id).all()

@vehicles.get("/{vehicle_id}", response_model=VehicleSchema)
def get_vehicle(policy_id: int, vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id, Vehicle.policy_id == policy_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@vehicles.put("/{vehicle_id}", response_model=VehicleSchema)
def update_vehicle(policy_id: int, vehicle_id: int, vehicle_update: VehicleUpdate, db: Session = Depends(get_db)):
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id, Vehicle.policy_id == policy_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Check duplicates
    update_data = vehicle_update.model_dump(exclude_unset=True)
    if "engine_no" in update_data and check_engine_duplicate(db, update_data["engine_no"], vehicle_id):
        raise HTTPException(status_code=400, detail="Engine number already exists")
    if "chassis_no" in update_data and check_chassis_duplicate(db, update_data["chassis_no"], vehicle_id):
        raise HTTPException(status_code=400, detail="Chassis number already exists")
    
    for field, value in update_data.items():
        setattr(db_vehicle, field, value)
    
    # Recalculate vehicle age if year changed
    if "year_of_manufacturing" in update_data:
        db_vehicle.vehicle_age = calculate_vehicle_age(db_vehicle.year_of_manufacturing)
    
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@vehicles.delete("/{vehicle_id}")
def delete_vehicle(policy_id: int, vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id, Vehicle.policy_id == policy_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db.delete(db_vehicle)
    db.commit()
    return {"message": "Vehicle deleted successfully"}

# Discounts Router (Item-level)
discounts = APIRouter(prefix="/api/policies/{policy_id}/items/{item_id}/discounts", tags=["discounts"])

@discounts.post("/", response_model=DiscountSchema)
def create_discount(policy_id: int, item_id: int, discount: DiscountCreate, db: Session = Depends(get_db)):
    discount_data = discount.model_dump()
    discount_data["item_id"] = item_id
    db_discount = Discount(**discount_data)
    db.add(db_discount)
    db.commit()
    db.refresh(db_discount)
    calculate_item_discounts(db, item_id)
    recalculate_policy(db, policy_id)
    return db_discount

@discounts.get("/", response_model=List[DiscountSchema])
def list_discounts(policy_id: int, item_id: int, db: Session = Depends(get_db)):
    return db.query(Discount).filter(Discount.item_id == item_id).all()

@discounts.delete("/{discount_id}")
def delete_discount(policy_id: int, item_id: int, discount_id: int, db: Session = Depends(get_db)):
    db_discount = db.query(Discount).filter(Discount.id == discount_id, Discount.item_id == item_id).first()
    if not db_discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    db.delete(db_discount)
    db.commit()
    calculate_item_discounts(db, item_id)
    recalculate_policy(db, policy_id)
    return {"message": "Discount deleted successfully"}

# Policy Discounts Router
policy_discounts = APIRouter(prefix="/api/policies/{policy_id}/policy-discounts", tags=["policy-discounts"])

@policy_discounts.post("/", response_model=PolicyDiscountSchema)
def create_policy_discount(policy_id: int, discount: PolicyDiscountCreate, db: Session = Depends(get_db)):
    discount_data = discount.model_dump()
    discount_data["policy_id"] = policy_id
    db_discount = PolicyDiscount(**discount_data)
    db.add(db_discount)
    db.commit()
    db.refresh(db_discount)
    recalculate_policy(db, policy_id)
    return db_discount

@policy_discounts.get("/", response_model=List[PolicyDiscountSchema])
def list_policy_discounts(policy_id: int, db: Session = Depends(get_db)):
    return db.query(PolicyDiscount).filter(PolicyDiscount.policy_id == policy_id).all()

@policy_discounts.delete("/{discount_id}")
def delete_policy_discount(policy_id: int, discount_id: int, db: Session = Depends(get_db)):
    db_discount = db.query(PolicyDiscount).filter(PolicyDiscount.id == discount_id, PolicyDiscount.policy_id == policy_id).first()
    if not db_discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    db.delete(db_discount)
    db.commit()
    recalculate_policy(db, policy_id)
    return {"message": "Discount deleted successfully"}

# Deductibles Router
deductibles = APIRouter(prefix="/api/policies/{policy_id}/deductibles", tags=["deductibles"])

@deductibles.post("/", response_model=DeductibleSchema)
def create_deductible(policy_id: int, deductible: DeductibleCreate, db: Session = Depends(get_db)):
    deductible_data = deductible.model_dump()
    deductible_data["policy_id"] = policy_id
    db_deductible = Deductible(**deductible_data)
    db.add(db_deductible)
    db.commit()
    db.refresh(db_deductible)
    return db_deductible

@deductibles.get("/", response_model=List[DeductibleSchema])
def list_deductibles(policy_id: int, db: Session = Depends(get_db)):
    return db.query(Deductible).filter(Deductible.policy_id == policy_id).all()

@deductibles.delete("/{deductible_id}")
def delete_deductible(policy_id: int, deductible_id: int, db: Session = Depends(get_db)):
    db_deductible = db.query(Deductible).filter(Deductible.id == deductible_id, Deductible.policy_id == policy_id).first()
    if not db_deductible:
        raise HTTPException(status_code=404, detail="Deductible not found")
    db.delete(db_deductible)
    db.commit()
    return {"message": "Deductible deleted successfully"}

# Clauses Router
clauses = APIRouter(prefix="/api/policies/{policy_id}/clauses", tags=["clauses"])

@clauses.post("/", response_model=ClauseSchema)
def create_clause(policy_id: int, clause: ClauseCreate, db: Session = Depends(get_db)):
    clause_data = clause.model_dump()
    clause_data["policy_id"] = policy_id
    db_clause = Clause(**clause_data)
    db.add(db_clause)
    db.commit()
    db.refresh(db_clause)
    return db_clause

@clauses.get("/", response_model=List[ClauseSchema])
def list_clauses(policy_id: int, db: Session = Depends(get_db)):
    return db.query(Clause).filter(Clause.policy_id == policy_id).all()

@clauses.put("/{clause_id}", response_model=ClauseSchema)
def update_clause(policy_id: int, clause_id: int, clause_update: ClauseUpdate, db: Session = Depends(get_db)):
    db_clause = db.query(Clause).filter(Clause.id == clause_id, Clause.policy_id == policy_id).first()
    if not db_clause:
        raise HTTPException(status_code=404, detail="Clause not found")
    for field, value in clause_update.model_dump(exclude_unset=True).items():
        setattr(db_clause, field, value)
    db.commit()
    db.refresh(db_clause)
    return db_clause

@clauses.delete("/{clause_id}")
def delete_clause(policy_id: int, clause_id: int, db: Session = Depends(get_db)):
    db_clause = db.query(Clause).filter(Clause.id == clause_id, Clause.policy_id == policy_id).first()
    if not db_clause:
        raise HTTPException(status_code=404, detail="Clause not found")
    db.delete(db_clause)
    db.commit()
    return {"message": "Clause deleted successfully"}

# Warranties Router
warranties = APIRouter(prefix="/api/policies/{policy_id}/warranties", tags=["warranties"])

@warranties.post("/", response_model=WarrantySchema)
def create_warranty(policy_id: int, warranty: WarrantyCreate, db: Session = Depends(get_db)):
    warranty_data = warranty.model_dump()
    warranty_data["policy_id"] = policy_id
    db_warranty = Warranty(**warranty_data)
    db.add(db_warranty)
    db.commit()
    db.refresh(db_warranty)
    return db_warranty

@warranties.get("/", response_model=List[WarrantySchema])
def list_warranties(policy_id: int, db: Session = Depends(get_db)):
    return db.query(Warranty).filter(Warranty.policy_id == policy_id).all()

@warranties.delete("/{warranty_id}")
def delete_warranty(policy_id: int, warranty_id: int, db: Session = Depends(get_db)):
    db_warranty = db.query(Warranty).filter(Warranty.id == warranty_id, Warranty.policy_id == policy_id).first()
    if not db_warranty:
        raise HTTPException(status_code=404, detail="Warranty not found")
    db.delete(db_warranty)
    db.commit()
    return {"message": "Warranty deleted successfully"}

# Agencies Router
agencies = APIRouter(prefix="/api/policies/{policy_id}/agencies", tags=["agencies"])

@agencies.post("/", response_model=AgencySchema)
def create_agency(policy_id: int, agency: AgencyCreate, db: Session = Depends(get_db)):
    agency_data = agency.model_dump()
    agency_data["policy_id"] = policy_id
    db_agency = Agency(**agency_data)
    db.add(db_agency)
    db.commit()
    db.refresh(db_agency)
    
    # Validate apportionment
    is_valid, error_msg = validate_agency_apportionment(db, policy_id)
    if not is_valid:
        db.delete(db_agency)
        db.commit()
        raise HTTPException(status_code=400, detail=error_msg)
    
    return db_agency

@agencies.get("/", response_model=List[AgencySchema])
def list_agencies(policy_id: int, db: Session = Depends(get_db)):
    return db.query(Agency).filter(Agency.policy_id == policy_id).all()

@agencies.delete("/{agency_id}")
def delete_agency(policy_id: int, agency_id: int, db: Session = Depends(get_db)):
    db_agency = db.query(Agency).filter(Agency.id == agency_id, Agency.policy_id == policy_id).first()
    if not db_agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    db.delete(db_agency)
    db.commit()
    return {"message": "Agency deleted successfully"}
