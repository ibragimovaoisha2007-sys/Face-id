from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class ClassRoom(Base):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    students = relationship("Student", back_populates="class_room")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    terminal_user_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    class_id: Mapped[int | None] = mapped_column(ForeignKey("classes.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    class_room = relationship("ClassRoom", back_populates="students")
    parents = relationship("StudentParent", back_populates="student")


class Parent(Base):
    __tablename__ = "parents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    telegram_chat_id: Mapped[int | None] = mapped_column(Integer)
    link_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)

    students = relationship("StudentParent", back_populates="parent")


class StudentParent(Base):
    __tablename__ = "student_parents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parents.id"), nullable=False)

    student = relationship("Student", back_populates="parents")
    parent = relationship("Parent", back_populates="students")


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    device_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(64), nullable=False)
    location: Mapped[str | None] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"
    __table_args__ = (
        UniqueConstraint("device_id", "source_event_id", name="uq_device_source_event"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int | None] = mapped_column(ForeignKey("students.id"))
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_event_id: Mapped[str] = mapped_column(String(128), nullable=False)
    raw_payload: Mapped[str | None] = mapped_column(String)

    student = relationship("Student")
    device = relationship("Device")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[str] = mapped_column(String(32), default="admin")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
