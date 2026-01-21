from datetime import date

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.routers import attendance, devices, hikvision, students, sync
from app.services.attendance import build_daily_report

app = FastAPI(title=settings.app_name)

app.include_router(devices.router)
app.include_router(hikvision.router)
app.include_router(sync.router)
app.include_router(students.router)
app.include_router(attendance.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": settings.app_name},
    )


@app.get("/admin/attendance", response_class=HTMLResponse)
def admin_attendance(
    request: Request,
    db: Session = Depends(get_db),
):
    raw_date = request.query_params.get("date")
    report_date = date.fromisoformat(raw_date) if raw_date else date.today()
    report = build_daily_report(db, report_date)
    return templates.TemplateResponse(
        "attendance.html",
        {"request": request, "records": report},
    )
