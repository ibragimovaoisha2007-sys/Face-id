from datetime import date, datetime, time
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import AttendanceLog, Student


def parse_late_time() -> time:
    hour, minute = settings.late_after_time.split(":")
    return time(int(hour), int(minute))


def build_daily_report(db: Session, report_date: date):
    start = datetime.combine(report_date, time.min)
    end = datetime.combine(report_date, time.max)
    late_cutoff = datetime.combine(report_date, parse_late_time())

    students = list(db.scalars(select(Student)))
    report = []

    for student in students:
        logs = list(
            db.scalars(
                select(AttendanceLog)
                .where(
                    and_(
                        AttendanceLog.student_id == student.id,
                        AttendanceLog.event_time >= start,
                        AttendanceLog.event_time <= end,
                    )
                )
                .order_by(AttendanceLog.event_time)
            )
        )
        first_in = next((log.event_time for log in logs if log.event_type == "IN"), None)
        last_out = next(
            (log.event_time for log in reversed(logs) if log.event_type == "OUT"),
            None,
        )
        is_late = bool(first_in and first_in > late_cutoff)

        report.append(
            {
                "student_id": student.id,
                "full_name": student.full_name,
                "first_in": first_in,
                "last_out": last_out,
                "is_late": is_late,
            }
        )

    return report
