import json
import re
from datetime import datetime
from fastapi import APIRouter, Request
from app import models
from app.db import SessionLocal
from app.telegram_bot import bot 

# Router obyektini yaratish
router = APIRouter(prefix="/hikvision", tags=["hikvision"])

@router.post("/event-receiver")
async def event_receiver(request: Request):
    db = SessionLocal()
    student_id_str = None
    try:
        # 1. Kelgan xom ma'lumotni o'qiymiz
        body_bytes = await request.body()
        body_str = body_bytes.decode('utf-8', errors='ignore')
        
        # 2. "employeeNo" (ID) ni qidiramiz
        # Bu Regex XML va JSON formatlari uchun optimallashgan
        id_match = re.search(r'("employeeNo"|<employeeNo>)\s*[:>]\s*"?([^"<, \s]+)"?', body_str)
        
        if id_match:
            student_id_str = id_match.group(2).strip()
            print("\n" + "⭐" * 40)
            print(f"✅ SIGNAL KELDI! Terminal yuborgan ID: {student_id_str}")
        else:
            # ID bo'lmasa, bu shunchaki texnik "heartbeat" signali
            return {"status": "heartbeat_ignored"}

        # 3. O'quvchini bazadan qidirish
        student = db.query(models.Student).filter(models.Student.terminal_user_id == student_id_str).first()
        
        if not student:
            print(f"⚠️ ID {student_id_str} bazada topilmadi!")
            print("⭐" * 40 + "\n")
            return {"status": "student_not_found"}

        print(f"👤 O'quvchi: {student.full_name}")

        # 4. Davomat logini saqlash
        log = models.AttendanceLog(
            student_id=student.id,
            event_type='ACCESS',
            event_time=datetime.now(),
            raw_payload=body_str[:1000]
        )
        db.add(log)
        db.commit()
        print("💾 Davomat bazaga yozildi.")

        # 5. Telegramga xabar yuborish
        parent_links = db.query(models.StudentParent).filter(models.StudentParent.student_id == student.id).all()
        for link in parent_links:
            parent = db.query(models.Parent).filter(models.Parent.id == link.parent_id).first()
            if parent and parent.telegram_chat_id:
                msg = (
                    f"🔔 **Maktab davomati**\n\n"
                    f"Farzandingiz **{student.full_name}** maktabga keldi.\n"
                    f"⏰ Vaqt: {datetime.now().strftime('%H:%M')}"
                )
                try:
                    await bot.send_message(chat_id=parent.telegram_chat_id, text=msg, parse_mode="Markdown")
                    print(f"🚀 Xabar yuborildi: {parent.full_name}")
                except Exception as tg_e:
                    print(f"❌ Telegram xato: {tg_e}")

    except Exception as e:
        print(f"❌ Tizimda xato: {str(e)}")
        db.rollback()
    finally:
        db.close()
        if student_id_str:
            print("⭐" * 40 + "\n")

    return {"status": "success"}
