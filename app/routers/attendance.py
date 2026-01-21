from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import AttendanceReport
from app.services.attendance import build_daily_report

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.get("/report", response_model=AttendanceReport)
def attendance_report(
    report_date: date = Query(..., alias="date"),
    db: Session = Depends(get_db),
):
    records = build_daily_report(db, report_date)
    return {"date": report_date.isoformat(), "records": records}
