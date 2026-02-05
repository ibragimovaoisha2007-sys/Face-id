import os
import sys

# Loyiha ildizini Python yo'liga qo'shamiz
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from app.db import SessionLocal
from app.models import Parent, Student, StudentParent

def add_parent():
    db = SessionLocal()
    try:
        # 1. O'zingizni ota-ona sifatida qo'shing
        # 'link_code' - botda ro'yxatdan o'tish uchun ixtiyoriy kod
        new_parent = Parent(
            full_name="Mening Akkauntim", 
            phone="+998901234567", # O'z raqamingiz
            link_code="TEST777",   # Botga yuboradigan kodingiz
            telegram_chat_id=None  # Botga yozganingizda avtomat to'ladi
        )
        db.add(new_parent)
        db.flush() # ID olish uchun

        # 2. Bazadagi birinchi o'quvchini topamiz
        student = db.query(Student).first()
        
        if student:
            # 3. O'zingizni shu o'quvchiga bog'lang
            link = StudentParent(
                student_id=student.id,
                parent_id=new_parent.id
            )
            db.add(link)
            db.commit()
            print(f"✅ Tayyor! O'quvchi: {student.full_name}")
            print(f"💡 Endi botga o'tib 'TEST777' kodini yuboring.")
        else:
            print("❌ Bazada o'quvchi topilmadi!")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Xato: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_parent()
