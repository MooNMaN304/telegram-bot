from src.db.database import SessionLocal
from src.cinemas.cinema_model import CinemaModel

db = SessionLocal()
cinemas = db.query(CinemaModel).all()

if not cinemas:
    print("❌ Таблица 'cinemas' пуста")
else:
    print("✅ Найдено кинотеатров:", len(cinemas))
    for c in cinemas:
        print(f"- {c.id}: {c.name} ({c.address})")

