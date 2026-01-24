from sqlalchemy import func
from datetime import date
from app.models import Student, AttendanceLog

def get_daily_stats(db):
    today = date.today()
    
    # 1. Bazadagi jami o'quvchilar sonini sanaymiz
    total_students = db.query(Student).count()
    
    # 2. Bugun kelgan o'quvchilarni (unikal holatda) sanaymiz
    present_students = db.query(AttendanceLog.student_id)\
        .filter(func.date(AttendanceLog.event_time) == today)\
        .filter(AttendanceLog.student_id.isnot(None))\
        .distinct().count()
    
    # 3. Foizni hisoblaymiz
    percent = (present_students / total_students * 100) if total_students > 0 else 0
        
    return {
        "total": total_students,
        "present": present_students,
        "absent": total_students - present_students,
        "percent": round(percent, 1)
    }
