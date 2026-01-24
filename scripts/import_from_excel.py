import pandas as pd
import random
import string
from app.db import SessionLocal
from app.models import Student, Parent, StudentParent

def import_students():
    db = SessionLocal()
    try:
        df = pd.read_excel("app/static/students.xlsx")
    except Exception as e:
        print(f"Xato: Excelni o'qib bo'lmadi: {e}")
        return

    for index, row in df.iterrows():
        try:
            full_name_str = f"{row['Ism']} {row['Familiya']}"
            t_id = str(row['ID'])
            
            student = Student(
                full_name=full_name_str, 
                terminal_user_id=t_id, 
                is_active=True
            )
            db.add(student)
            db.flush()
            
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            parent = Parent(
                full_name=f"{full_name_str} ota-onasi", 
                link_code=code,
                phone=f"temp_{t_id}", 
                telegram_chat_id=None
            )
            db.add(parent)
            db.flush()
            
            sp = StudentParent(student_id=student.id, parent_id=parent.id)
            db.add(sp)
            print(f"✅ Qo'shildi: {full_name_str} (ID: {t_id})")
            
        except Exception as e:
            print(f"❌ Xato (ID {row['ID']}): {e}")
            db.rollback()
            continue

    db.commit()
    db.close()
    print("\n🚀 Barcha o'quvchilar muvaffaqiyatli saqlandi!")

if __name__ == "__main__":
    import_students()
