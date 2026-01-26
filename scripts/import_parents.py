import os
import sys
import uuid

# Loyiha ildizini Python yo'liga qo'shamiz
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from app.db import SessionLocal
from app.models import Parent, Student, StudentParent

def start_import():
    db = SessionLocal()
    
    # Faqat sizning ma'lumotlaringiz qoldi
    parents_data = [
        {
            "name": "Oishaning Dadasi", 
            "phone": "998901234567",    
            "student_terminal_id": "40" # Kameradagi Employee ID
        },
    ]

    try:
        count = 0
        for data in parents_data:
            # 1. Kod generatsiya qilish
            l_code = str(uuid.uuid4())[:8].upper()
            
            # 2. Ota-onani yaratish
            parent = Parent(
                full_name=data['name'],
                phone=data['phone'],
                link_code=l_code
            )
            db.add(parent)
            db.flush()

            # 3. Bolani terminal_user_id orqali qidirish
            student = db.query(Student).filter(Student.terminal_user_id == data['student_terminal_id']).first()
            
            if student:
                # 4. Bog'lash
                link = StudentParent(student_id=student.id, parent_id=parent.id)
                db.add(link)
                count += 1
                print(f"✅ {student.full_name} <-> {parent.full_name} | KOD: {l_code}")
            else:
                print(f"⚠️ Bola topilmadi: ID {data['student_terminal_id']}")
        
        db.commit()
        print(f"\n🎉 Jami {count} ta ota-ona bazaga kiritildi va bog'landi!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Xato: {e}")
    finally:
        db.close()
    
if __name__ == "__main__":
    start_import()
