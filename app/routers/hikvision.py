import json
import asyncio
from datetime import datetime
from fastapi import APIRouter, Request
from app import models
from app.db import SessionLocal
from app.config import settings
from app.services.hikvision_adapter import GenericHikvisionAdapter
from app.telegram_bot import bot 

router = APIRouter(prefix="/hikvision", tags=["hikvision"])

@router.post("/event-receiver")
async def event_receiver(request: Request):
    payload = await request.json()
    asyncio.create_task(process_event(payload))
    return {"status": "received"}

async def process_event(payload):
    db = SessionLocal()
    try:
        adapter = GenericHikvisionAdapter()
        normalized = adapter.normalize(payload)

        # 1. Qurilmani tekshirish
        device_id = str(normalized.device_id) if normalized.device_id else "UNKNOWN-DEV"
        device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
        
        if not device:
            device = models.Device(
                device_id=device_id, 
                name="Auto Device", 
                ip_address="127.0.0.1",
                location="Main Gate",
                is_active=True
            )
            db.add(device)
            db.commit()
            db.refresh(device)

        # 2. O'quvchini qidirish
        student_id_str = str(normalized.terminal_user_id)
        # O'quvchini ota-onalari bilan birga yuklaymiz (relationship orqali)
        student = db.query(models.Student).filter(models.Student.terminal_user_id == student_id_str).first()

        # 3. Log yozish
        log = models.AttendanceLog(
            student_id=student.id if student else None,
            device_id=device.id,
            event_type=getattr(normalized, 'event_type', 'ACCESS') or 'ACCESS',
            event_time=getattr(normalized, 'event_time', datetime.now()),
            source_event_id=str(getattr(normalized, 'source_event_id', '0')),
            raw_payload=json.dumps(payload)
        )
        db.add(log)
        db.commit()

        # 4. Telegram xabar (Ota-onaga yuborish qismi)
        if student:
            # O'quvchiga biriktirilgan ota-onalarni topish
            student_parents = db.query(models.StudentParent).filter(models.StudentParent.student_id == student.id).all()
            
            status_text = "maktabga keldi ✅" if "IN" in log.event_type.upper() else "maktabdan ketdi 🏠"
            msg = f"🔔 **Davomat xabari**\n\nFarzandingiz **{student.full_name}** hozirgina {status_text}."

            for link in student_parents:
                parent = db.query(models.Parent).get(link.parent_id)
                if parent and parent.telegram_chat_id:
                    try:
                        await bot.send_message(chat_id=parent.telegram_chat_id, text=msg, parse_mode="Markdown")
                    except Exception as tg_e:
                        print(f"Telegram yuborishda xato (ChatID: {parent.telegram_chat_id}): {tg_e}")
        
        # Admin uchun log (ixtiyoriy)
        elif settings.telegram_admin_chat_id:
             await bot.send_message(chat_id=settings.telegram_admin_chat_id, text=f"❓ Noma'lum ID ({student_id_str}) terminalda ko'rindi.")

    except Exception as e:
        print(f"ISHLOV BERISHDA XATO: {str(e)}")
        db.rollback()
    finally:
        db.close()
