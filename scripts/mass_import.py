import sys
import os
import pandas as pd
import uuid
from app.db import SessionLocal
from app import models

# Loyiha ildiz papkasini Python yo'liga qo'shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def import_students_and_parents(file_path):
    db = SessionLocal()
    try:
        # Fayl borligini tekshirish
        if not os.path.exists(file_path):
            print(f"❌ Xato: {file_path} topilmadi!")
            return

        # Excel faylini o'qiymiz
        df = pd.read_excel(file_path)
        
        for index, row in df.iterrows():
            # 1. O'quvchini qo'shish
            student = models.Student(
                full_name=row['oquvchi_ismi'],
                terminal_user_id=str(row['terminal_id'])
            )
            db.add(student)
            db.flush() 

            # 2. Ota-onani qo'shish (PHONE QISMI QO'SHILDI)
            link_code = str(uuid.uuid4().hex[:8].upper())
            
            # Exceldan phone ni o'qiymiz, agar bo'sh bo'lsa vaqtinchalik raqam beramiz
            phone_val = str(row['phone']) if pd.notna(row.get('phone')) else f"+99800{row['terminal_id']}"
            
            parent = models.Parent(
                full_name=row['ota_ona_ismi'],
                phone=phone_val,  # <--- Mana shu joyi yetishmayotgan edi
                link_code=link_code
            )
            db.add(parent)
            db.flush()

            # 3. Ularni bir-biriga bog'lash
            link = models.StudentParent(
                student_id=student.id,
                parent_id=parent.id
            )
            db.add(link)
            
            print(f"✅ {row['oquvchi_ismi']} yuklandi. Kod: {link_code}")

        db.commit()
        print("\n🎉 Ma'lumotlar muvaffaqiyatli bazaga qo'shildi!")
    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_students_and_parents("scripts/students.xlsx")
