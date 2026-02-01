from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db

from app.services.monitor_service import MonitorService
from app.services.sync_service import SyncService

router = APIRouter()
monitor_service = MonitorService()
sync_service = SyncService()

@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    # In a real app, we might pass db to the service
    return monitor_service.get_stats()

@router.get("/executions")
def get_executions(db: Session = Depends(get_db)):
    # For now return list from DB (mock implementation in service was stats only)
    # We can expand MonitorService or just query here.
    # Let's keep it simple and consistent with previous behavior but using DB
    from app.models import Execution
    return db.query(Execution).limit(50).all()

@router.post("/sync")
def trigger_sync(source: str = "postgres", destination: str = "sheets"):
    return sync_service.sync_data(source, destination)
