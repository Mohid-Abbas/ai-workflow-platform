from sqlalchemy.orm import Session
from app.models import Execution
from app.core.database import SessionLocal

class MonitorService:
    def check_health(self):
        return {"status": "ok", "database": "connected"}

    def get_stats(self):
        db: Session = SessionLocal()
        try:
            total_executions = db.query(Execution).count()
            failed_executions = db.query(Execution).filter(Execution.status == "failed").count()
            return {
                "total_executions": total_executions,
                "failed_executions": failed_executions,
                "success_rate": 1.0 - (failed_executions / total_executions) if total_executions > 0 else 0
            }
        finally:
            db.close()
