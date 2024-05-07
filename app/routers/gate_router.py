from fastapi import APIRouter, Depends, Path, Response, status
from app import schemas, models, database
from sqlalchemy.orm import Session
import uuid

router = APIRouter(tags=["Gates"])

get_db = database.get_db

@router.post("/gates")
def create_gate(response: Response, gate: schemas.Gate, db: Session = Depends(get_db),):
    gate_id = str(uuid.uuid4())
    new_gate = models.Gate(gate_id=gate_id, name=gate.name, current_state=False)
    db.add(new_gate)
    db.commit()
    db.refresh(new_gate)

    return new_gate