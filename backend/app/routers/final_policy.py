"""
Computational Sheet, Final Policy, Reminders, Gmail Integration routers
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.computational_sheet import generate_computational_sheet
from app.services.policy_generator import generate_final_policy, generate_cover_letter, generate_policy_document
from app.services.pdf_generator import html_to_pdf
from app.services.reminder_service import process_reminders
from app.services.gmail_service import get_auth_url, handle_oauth_callback, fetch_unread_emails
from app.models.reminder import Reminder
from app.models.policy import Policy, PolicyStatus
from typing import List
import asyncio

# Computational Sheet Router
computational_sheet = APIRouter(prefix="/api/policies/{policy_id}/computational-sheet", tags=["computational-sheet"])

@computational_sheet.get("/")
def get_computational_sheet(policy_id: int, db: Session = Depends(get_db)):
    """Get read-only computational sheet with all aggregated data"""
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    sheet = generate_computational_sheet(db, policy_id)
    return sheet

# Final Policy Router
final_policy = APIRouter(prefix="/api/policies/{policy_id}/final-policy", tags=["final-policy"])

@final_policy.get("/")
def get_final_policy(policy_id: int, db: Session = Depends(get_db)):
    """Get complete final policy data as JSON"""
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    policy_data = generate_final_policy(db, policy_id)
    return policy_data

@final_policy.get("/pdf")
def download_policy_pdf(policy_id: int, db: Session = Depends(get_db)):
    """Download policy document as PDF"""
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    html_content = generate_policy_document(db, policy_id)
    pdf_bytes = html_to_pdf(html_content)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=policy_{policy.policy_number}.pdf"
        }
    )

@final_policy.get("/cover-letter/pdf")
def download_cover_letter_pdf(policy_id: int, db: Session = Depends(get_db)):
    """Download cover letter as PDF"""
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    html_content = generate_cover_letter(db, policy_id)
    pdf_bytes = html_to_pdf(html_content)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=cover_letter_{policy.policy_number}.pdf"
        }
    )

# Reminders Router
reminders = APIRouter(prefix="/api/reminders", tags=["reminders"])

@reminders.get("/")
def list_reminders(db: Session = Depends(get_db)):
    """List all reminders with status"""
    reminders = db.query(Reminder).all()
    return [
        {
            "id": r.id,
            "client_name": r.client_name,
            "email": r.email,
            "phone": r.phone,
            "due_amount": float(r.due_amount),
            "due_date": r.due_date.isoformat(),
            "reminder_sent": r.reminder_sent,
            "last_reminder_at": r.last_reminder_at.isoformat() if r.last_reminder_at else None
        }
        for r in reminders
    ]

@reminders.post("/trigger")
async def trigger_reminders(db: Session = Depends(get_db)):
    """Manual trigger for testing reminder job"""
    result = await process_reminders(db)
    return result

# Gmail Integration Router
gmail_integration = APIRouter(prefix="/api/gmail", tags=["gmail-integration"])

@gmail_integration.get("/auth-url")
def get_gmail_auth_url():
    """Get OAuth 2.0 authorization URL"""
    try:
        auth_url = get_auth_url()
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@gmail_integration.get("/callback")
def gmail_callback(code: str, db: Session = Depends(get_db)):
    """OAuth callback endpoint"""
    try:
        tokens = handle_oauth_callback(code)
        return {"message": "Authentication successful", "tokens": tokens}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@gmail_integration.post("/poll")
async def poll_gmail(db: Session = Depends(get_db)):
    """Manual trigger for Gmail polling (for testing)"""
    try:
        from app.automation.gmail_poller import run_gmail_poller
        await run_gmail_poller()
        return {"message": "Gmail polling completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@gmail_integration.get("/drafts")
def get_draft_policies(db: Session = Depends(get_db)):
    """List auto-created draft policies from emails"""
    draft_policies = db.query(Policy).filter(
        Policy.status == PolicyStatus.DRAFT,
        Policy.notes.like("%Auto-created from email%")
    ).all()
    
    return [
        {
            "id": p.id,
            "policy_number": p.policy_number,
            "client_id": p.client_id,
            "notes": p.notes,
            "created_at": p.created_at.isoformat()
        }
        for p in draft_policies
    ]
