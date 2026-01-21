from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.db import get_db

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/register", response_model=schemas.DeviceOut)
def register_device(payload: schemas.DeviceCreate, db: Session = Depends(get_db)):
    existing = crud.get_device_by_device_id(db, payload.device_id)
    if existing:
        raise HTTPException(status_code=400, detail="Device already registered")
    device = models.Device(**payload.model_dump())
    return crud.create_device(db, device)
