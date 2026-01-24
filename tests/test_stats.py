import pytest
from app.db import SessionLocal
from app.services.stats import get_daily_stats

# Bazaga ulanishni tekshirish
def test_db_connection():
    db = SessionLocal()
    try:
        assert db is not None
    finally:
        db.close()

# Statistika logikasini tekshirish
def test_stats_return_types():
    db = SessionLocal()
    try:
        stats = get_daily_stats(db)
        # Natija lug'at (dict) ekanligini tekshiramiz
        assert isinstance(stats, dict)
        # Kerakli kalitlar borligini tekshiramiz
        assert "total" in stats
        assert "present" in stats
        assert "percent" in stats
        # Foiz 0 va 100 oralig'ida ekanligini tekshiramiz
        assert 0 <= stats["percent"] <= 100
    finally:
        db.close()
