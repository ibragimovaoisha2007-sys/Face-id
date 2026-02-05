import time
import asyncio
import os
import sys

# Loyiha ildizini qo'shish
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from app.db import SessionLocal
from app.models import AttendanceLog, StudentParent, Parent, Student
from app.telegram_bot import bot

async def check_new_logs():
    print("🚀 Xabarnoma xizmati ishga tushdi...")
    last_checked_id = 0
    
    # Avval bazadagi oxirgi IDni olamiz
    db = SessionLocal()
    last_log = db.query(AttendanceLog).order_by(AttendanceLog.id.desc()).first()
    if last_log:
        last_checked_id = last_log.id
    db.close()

    while True:
        db = SessionLocal()
        # Faqat biz ko'rmagan yangi loglarni qidiramiz
        new_logs = db.query(AttendanceLog).filter(AttendanceLog.id > last_checked_id).all()
        
        for log in new_logs:
            # O'quvchining ota-onalarini topamiz
            parent_links = db.query(StudentParent).filter(StudentParent.student_id == log.student_id).all()
            student = db.query(Student).get(log.student_id)
            
            for link in parent_links:
                parent = db.query(Parent).get(link.parent_id)
                if parent and parent.telegram_chat_id:
                    status = "keldi ✅" if log.event_type == "IN" else "ketdi 🏠"
                    message = f"🔔 **Davomat xabari**\n\n👤 O'quvchi: {student.full_name}\n🕒 Vaqt: {log.event_time.strftime('%H:%M')}\n📍 Holat: Maktabga {status}"
                    
                    try:
                        await bot.send_message(chat_id=parent.telegram_chat_id, text=message, parse_mode="Markdown")
                        print(f"📧 Xabar yuborildi: {parent.full_name} ({student.full_name})")
                    except Exception as e:
                        print(f"❌ Xabar yuborishda xato: {e}")
            
            last_checked_id = log.id
        
        db.close()
        await asyncio.sleep(2) # Har 2 soniyada tekshiradi

if __name__ == "__main__":
    asyncio.run(check_new_logs())
