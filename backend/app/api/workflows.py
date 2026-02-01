from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Workflow, Execution
from pydantic import BaseModel
from app.api.auth import get_current_user

router = APIRouter()

class WorkflowBase(BaseModel):
    name: str
    config: dict

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowRead(WorkflowBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

@router.post("/", response_model=WorkflowRead)
def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_workflow = Workflow(name=workflow.name, config=workflow.config, owner_id=current_user["id"])
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

@router.get("/", response_model=List[WorkflowRead])
def read_workflows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    workflows = db.query(Workflow).filter(Workflow.owner_id == current_user["id"]).offset(skip).limit(limit).all()
    return workflows

@router.get("/{workflow_id}", response_model=WorkflowRead)
def read_workflow(workflow_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id, Workflow.owner_id == current_user["id"]).first()
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.post("/{workflow_id}/execute")
def execute_workflow(workflow_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
         raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Mock execution
    execution = Execution(workflow_id=workflow.id, status="running", logs={"step": "init"})
    db.add(execution)
    db.commit()
    db.refresh(execution)
    return {"message": "Workflow execution started", "execution_id": execution.id}
