from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models


def create_device(db: Session, device: models.Device) -> models.Device:
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def get_device_by_device_id(db: Session, device_id: str) -> models.Device | None:
    return db.scalar(select(models.Device).where(models.Device.device_id == device_id))


def create_student(db: Session, student: models.Student) -> models.Student:
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def list_students(db: Session) -> list[models.Student]:
    return list(db.scalars(select(models.Student)))


def get_student_by_terminal_id(db: Session, terminal_user_id: str) -> models.Student | None:
    return db.scalar(
        select(models.Student).where(models.Student.terminal_user_id == terminal_user_id)
    )


def create_attendance_log(db: Session, log: models.AttendanceLog) -> models.AttendanceLog:
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
