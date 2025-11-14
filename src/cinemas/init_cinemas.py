import logging
from src.db.database import SessionLocal
from src.cinemas.cinema_model import CinemaModel
from src.cinemas.cinema_repository import CinemaRepository

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CINEMAS = [
    {"name": "Малибу", "address": "г. Липецк, ул. Терешковой, 35б, ТРЦ «Малибу»"},
    {"name": "КИНОМАКС", "address": "г. Липецк, ул. Катукова, 51, ТРЦ «Ривьера»"},
    {"name": "Кинолюкс", "address": "г. Липецк, ул. Титова, 10, ТРЦ «Москва»"},
    {"name": "Остров капитана Флинта", "address": "г. Липецк, ул. Студеновская, 124а, ТРЦ «Липецк»"},
]

def init_cinemas(db):
    """
    Проверяет наличие кинотеатров в БД и создает их, если отсутствуют.
    """
    logger.info("Проверка наличия кинотеатров...")
    repo = CinemaRepository(db=db, cinema_model=CinemaModel)

    for cinema_data in CINEMAS:
        cinema, created = repo.get_or_create(cinema_data)
        if created:
            logger.info(f"🆕 Добавлен новый кинотеатр: {cinema.name} (id={cinema.id})")
        else:
            logger.info(f"✅ Кинотеатр '{cinema.name}' уже есть в базе (id={cinema.id})")

    logger.info("Проверка кинотеатров завершена.")


if __name__ == "__main__":
    db = SessionLocal()
    init_cinemas(db)
    db.close()
