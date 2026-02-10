"""
Banks, Product Setup, Items, Perils routers - Combined for efficiency
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.bank import Bank
from app.models.product_setup import ProductSetup
from app.models.item_detail import ItemDetail
from app.models.peril_calculation import PerilCalculation
from app.schemas.bank import Bank as BankSchema, BankCreate, BankUpdate
from app.schemas.product_setup import ProductSetup as ProductSetupSchema, ProductSetupCreate, ProductSetupUpdate
from app.schemas.item_detail import ItemDetail as ItemDetailSchema, ItemDetailCreate, ItemDetailUpdate
from app.schemas.peril_calculation import PerilCalculation as PerilCalculationSchema, PerilCalculationCreate, PerilCalculationUpdate
from app.services.premium_calculator import calculate_item_basic_premium, recalculate_policy, calculate_peril_premium

# Banks Router
banks = APIRouter(prefix="/api/policies/{policy_id}/banks", tags=["banks"])

@banks.post("/", response_model=BankSchema)
def create_bank(policy_id: int, bank: BankCreate, db: Session = Depends(get_db)):
    bank_data = bank.model_dump()
    bank_data["policy_id"] = policy_id
    db_bank = Bank(**bank_data)
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank

@banks.get("/", response_model=List[BankSchema])
def list_banks(policy_id: int, db: Session = Depends(get_db)):
    return db.query(Bank).filter(Bank.policy_id == policy_id).all()

@banks.get("/{bank_id}", response_model=BankSchema)
def get_bank(policy_id: int, bank_id: int, db: Session = Depends(get_db)):
    bank = db.query(Bank).filter(Bank.id == bank_id, Bank.policy_id == policy_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank

@banks.put("/{bank_id}", response_model=BankSchema)
def update_bank(policy_id: int, bank_id: int, bank_update: BankUpdate, db: Session = Depends(get_db)):
    db_bank = db.query(Bank).filter(Bank.id == bank_id, Bank.policy_id == policy_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    for field, value in bank_update.model_dump(exclude_unset=True).items():
        setattr(db_bank, field, value)
    db.commit()
    db.refresh(db_bank)
    return db_bank

@banks.delete("/{bank_id}")
def delete_bank(policy_id: int, bank_id: int, db: Session = Depends(get_db)):
    db_bank = db.query(Bank).filter(Bank.id == bank_id, Bank.policy_id == policy_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    db.delete(db_bank)
    db.commit()
    return {"message": "Bank deleted successfully"}

# Product Setup Router
product_setup = APIRouter(prefix="/api/policies/{policy_id}/product-setup", tags=["product-setup"])

@product_setup.post("/", response_model=ProductSetupSchema)
def create_product_setup(policy_id: int, setup: ProductSetupCreate, db: Session = Depends(get_db)):
    setup_data = setup.model_dump()
    setup_data["policy_id"] = policy_id
    db_setup = ProductSetup(**setup_data)
    db.add(db_setup)
    db.commit()
    db.refresh(db_setup)
    recalculate_policy(db, policy_id)
    return db_setup

@product_setup.get("/", response_model=ProductSetupSchema)
def get_product_setup(policy_id: int, db: Session = Depends(get_db)):
    setup = db.query(ProductSetup).filter(ProductSetup.policy_id == policy_id).first()
    if not setup:
        raise HTTPException(status_code=404, detail="Product setup not found")
    return setup

@product_setup.put("/", response_model=ProductSetupSchema)
def update_product_setup(policy_id: int, setup_update: ProductSetupUpdate, db: Session = Depends(get_db)):
    db_setup = db.query(ProductSetup).filter(ProductSetup.policy_id == policy_id).first()
    if not db_setup:
        raise HTTPException(status_code=404, detail="Product setup not found")
    for field, value in setup_update.model_dump(exclude_unset=True).items():
        setattr(db_setup, field, value)
    db.commit()
    db.refresh(db_setup)
    recalculate_policy(db, policy_id)
    return db_setup

# Items Router
items = APIRouter(prefix="/api/policies/{policy_id}/items", tags=["items"])

@items.post("/", response_model=ItemDetailSchema)
def create_item(policy_id: int, item: ItemDetailCreate, db: Session = Depends(get_db)):
    item_data = item.model_dump()
    item_data["policy_id"] = policy_id
    db_item = ItemDetail(**item_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    recalculate_policy(db, policy_id)
    return db_item

@items.get("/", response_model=List[ItemDetailSchema])
def list_items(policy_id: int, db: Session = Depends(get_db)):
    return db.query(ItemDetail).filter(ItemDetail.policy_id == policy_id).all()

@items.get("/{item_id}", response_model=ItemDetailSchema)
def get_item(policy_id: int, item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemDetail).filter(ItemDetail.id == item_id, ItemDetail.policy_id == policy_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@items.put("/{item_id}", response_model=ItemDetailSchema)
def update_item(policy_id: int, item_id: int, item_update: ItemDetailUpdate, db: Session = Depends(get_db)):
    db_item = db.query(ItemDetail).filter(ItemDetail.id == item_id, ItemDetail.policy_id == policy_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in item_update.model_dump(exclude_unset=True).items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    recalculate_policy(db, policy_id)
    return db_item

@items.delete("/{item_id}")
def delete_item(policy_id: int, item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDetail).filter(ItemDetail.id == item_id, ItemDetail.policy_id == policy_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    recalculate_policy(db, policy_id)
    return {"message": "Item deleted successfully"}

# Perils Router
perils = APIRouter(prefix="/api/policies/{policy_id}/items/{item_id}/perils", tags=["perils"])

@perils.post("/", response_model=PerilCalculationSchema)
def create_peril(policy_id: int, item_id: int, peril: PerilCalculationCreate, db: Session = Depends(get_db)):
    peril_data = peril.model_dump()
    peril_data["item_id"] = item_id
    
    # Calculate basic premium
    basic_premium = calculate_peril_premium(
        peril_data["base_value"],
        peril_data["rate_percent"],
        peril_data["percent_of_rate"],
        peril_data["calculation_basis"],
        peril_data["flat_amount"]
    )
    peril_data["basic_premium"] = basic_premium
    
    db_peril = PerilCalculation(**peril_data)
    db.add(db_peril)
    db.commit()
    db.refresh(db_peril)
    
    # Recalculate item and policy
    calculate_item_basic_premium(db, item_id)
    recalculate_policy(db, policy_id)
    
    return db_peril

@perils.get("/", response_model=List[PerilCalculationSchema])
def list_perils(policy_id: int, item_id: int, db: Session = Depends(get_db)):
    return db.query(PerilCalculation).filter(PerilCalculation.item_id == item_id).all()

@perils.get("/{peril_id}", response_model=PerilCalculationSchema)
def get_peril(policy_id: int, item_id: int, peril_id: int, db: Session = Depends(get_db)):
    peril = db.query(PerilCalculation).filter(PerilCalculation.id == peril_id, PerilCalculation.item_id == item_id).first()
    if not peril:
        raise HTTPException(status_code=404, detail="Peril not found")
    return peril

@perils.put("/{peril_id}", response_model=PerilCalculationSchema)
def update_peril(policy_id: int, item_id: int, peril_id: int, peril_update: PerilCalculationUpdate, db: Session = Depends(get_db)):
    db_peril = db.query(PerilCalculation).filter(PerilCalculation.id == peril_id, PerilCalculation.item_id == item_id).first()
    if not db_peril:
        raise HTTPException(status_code=404, detail="Peril not found")
    
    for field, value in peril_update.model_dump(exclude_unset=True).items():
        setattr(db_peril, field, value)
    
    # Recalculate basic premium
    db_peril.basic_premium = calculate_peril_premium(
        db_peril.base_value,
        db_peril.rate_percent,
        db_peril.percent_of_rate,
        db_peril.calculation_basis,
        db_peril.flat_amount
    )
    
    db.commit()
    db.refresh(db_peril)
    
    # Recalculate item and policy
    calculate_item_basic_premium(db, item_id)
    recalculate_policy(db, policy_id)
    
    return db_peril

@perils.delete("/{peril_id}")
def delete_peril(policy_id: int, item_id: int, peril_id: int, db: Session = Depends(get_db)):
    db_peril = db.query(PerilCalculation).filter(PerilCalculation.id == peril_id, PerilCalculation.item_id == item_id).first()
    if not db_peril:
        raise HTTPException(status_code=404, detail="Peril not found")
    db.delete(db_peril)
    db.commit()
    
    # Recalculate item and policy
    calculate_item_basic_premium(db, item_id)
    recalculate_policy(db, policy_id)
    
    return {"message": "Peril deleted successfully"}
