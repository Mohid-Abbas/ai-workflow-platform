from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Webhook

router = APIRouter()

@router.post("/incoming/{token}")
def trigger_webhook(token: str, payload: dict, db: Session = Depends(get_db)):
    # Log webhook
    webhook = Webhook(endpoint=token, payload=payload, status_code=200)
    db.add(webhook)
    db.commit()
    return {"status": "received"}

@router.get("/status/{id}")
def webhook_status(id: int, db: Session = Depends(get_db)):
    webhook = db.query(Webhook).filter(Webhook.id == id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return {"id": webhook.id, "status": "processed"}
