"""
Policies router
CRUD operations for policies
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.policy import Policy, generate_policy_number
from app.models.clause import Clause, DEFAULT_CLAUSES
from app.schemas.policy import Policy as PolicySchema, PolicyCreate, PolicyUpdate
from app.services.premium_calculator import recalculate_policy

router = APIRouter(prefix="/api/policies", tags=["policies"])


@router.post("/", response_model=PolicySchema)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    """Create a new policy"""
    policy_data = policy.model_dump()
    policy_data["policy_number"] = generate_policy_number()
    
    db_policy = Policy(**policy_data)
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    
    # Create default clauses
    for clause_name in DEFAULT_CLAUSES:
        clause = Clause(
            policy_id=db_policy.id,
            clause_name=clause_name,
            is_checked=False
        )
        db.add(clause)
    db.commit()
    
    return db_policy


@router.get("/", response_model=List[PolicySchema])
def list_policies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all policies"""
    policies = db.query(Policy).offset(skip).limit(limit).all()
    return policies


@router.get("/{policy_id}", response_model=PolicySchema)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    """Get a specific policy"""
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


@router.put("/{policy_id}", response_model=PolicySchema)
def update_policy(policy_id: int, policy_update: PolicyUpdate, db: Session = Depends(get_db)):
    """Update a policy"""
    db_policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not db_policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    # Update fields
    for field, value in policy_update.model_dump(exclude_unset=True).items():
        setattr(db_policy, field, value)
    
    db.commit()
    db.refresh(db_policy)
    return db_policy


@router.delete("/{policy_id}")
def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    """Delete a policy"""
    db_policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not db_policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    db.delete(db_policy)
    db.commit()
    return {"message": "Policy deleted successfully"}


@router.post("/{policy_id}/recalculate")
def recalculate_policy_endpoint(policy_id: int, db: Session = Depends(get_db)):
    """Recalculate policy premiums"""
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    recalculate_policy(db, policy_id)
    db.refresh(policy)
    
    return {
        "message": "Policy recalculated successfully",
        "gross_premium": float(policy.gross_premium),
        "net_premium": float(policy.net_premium),
        "sum_insured": float(policy.sum_insured)
    }
