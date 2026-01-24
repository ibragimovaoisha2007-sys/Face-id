import os
import sys
from sqlalchemy import text

# Loyiha ildizini qo'shish
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from app.db import engine

def update_database():
    with engine.connect() as conn:
        print("Baza ustuni yangilanmoqda...")
        conn.execute(text('ALTER TABLE parents ALTER COLUMN telegram_chat_id TYPE BIGINT'))
        conn.commit()
        print("✅ Bo'ldi! telegram_chat_id endi BIGINT bo'ldi.")

if __name__ == "__main__":
    update_database()
