import json
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, models
from app.config import settings
from app.db import get_db
from app.services.hikvision_adapter import GenericHikvisionAdapter

router = APIRouter(prefix="/hikvision", tags=["hikvision"])


@router.post("/event-receiver")
async def event_receiver(
    request: Request,
    db: Session = Depends(get_db),
    x_device_token: str | None = Header(default=None),
):
    if x_device_token and x_device_token != settings.hikvision_event_token:
        raise HTTPException(status_code=403, detail="Invalid device token")

    payload = await request.json()
    adapter = GenericHikvisionAdapter()
    normalized = adapter.normalize(payload)

    device = crud.get_device_by_device_id(db, normalized.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not registered")

    student = None
    if normalized.terminal_user_id:
        student = crud.get_student_by_terminal_id(db, normalized.terminal_user_id)

    log = models.AttendanceLog(
        student_id=student.id if student else None,
        device_id=device.id,
        event_type=normalized.event_type,
        event_time=normalized.event_time,
        source_event_id=normalized.source_event_id,
        raw_payload=json.dumps(normalized.raw_payload),
    )

    try:
        crud.create_attendance_log(db, log)
    except IntegrityError:
        db.rollback()
        return {"status": "duplicate"}

    return {"status": "ok"}
