import pandas as pd
import sys
import os

# Loyiha ildizini Python yo'liga qo'shamiz
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from app.db import SessionLocal
from app.models import Student

def start_import():
    db = SessionLocal()
    file_path = os.path.join(BASE_DIR, "app", "static", "students.xlsx")
    
    if not os.path.exists(file_path):
        print(f"❌ Xato: {file_path} topilmadi!")
        return

    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        df.columns = [c.strip() for c in df.columns] 
        
        count = 0
        for _, row in df.iterrows():
            # Modelga moslab Ism va Familiyani birlashtiramiz
            full_name_str = f"{row['Ism']} {row['Familiya']}"
            
            student = Student(
                terminal_user_id=str(row['ID']),
                full_name=full_name_str,  # Models.py dagi ustun nomi
                is_active=True
            )
            db.merge(student)
            count += 1
        
        db.commit()
        print(f"✅ Tayyor! {count} ta o'quvchi bazaga kiritildi.")
    except Exception as e:
        print(f"❌ Xato berdi: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    start_import()
