from datetime import datetime
from pydantic import BaseModel, Field


class DeviceCreate(BaseModel):
    name: str
    device_id: str
    ip_address: str
    location: str | None = None


class DeviceOut(BaseModel):
    id: int
    name: str
    device_id: str
    ip_address: str
    location: str | None = None

    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    full_name: str
    terminal_user_id: str
    class_id: int | None = None


class StudentOut(BaseModel):
    id: int
    full_name: str
    terminal_user_id: str
    class_id: int | None
    is_active: bool

    class Config:
        from_attributes = True


class AttendanceEventIn(BaseModel):
    terminal_user_id: str | None = None
    event_time: datetime
    device_id: str
    event_type: str
    source_event_id: str
    raw_payload: dict = Field(default_factory=dict)


class AttendanceReportItem(BaseModel):
    student_id: int
    full_name: str
    first_in: datetime | None
    last_out: datetime | None
    is_late: bool


class AttendanceReport(BaseModel):
    date: str
    records: list[AttendanceReportItem]
