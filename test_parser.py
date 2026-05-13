#!/usr/bin/env python3
"""
Скрипт для тестирования парсера с очисткой БД
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.logger import setup_logging, get_logger
from src.db.database import engine
from src.base.base_model import Base
from src.parsing_movie.kinomax_cinema.controller import KinomaxController
from src.parsing_movie.malibu_cinema.controller import MalibuController

logger = get_logger(__name__)

def clear_database():
    """Очищает все таблицы в БД"""
    logger.info("Очищаю БД...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logger.info("БД очищена и пересоздана!")

def run_parsers():
    """Запускает парсеры"""
    try:
        logger.info("=" * 80)
        logger.info("ЗАПУСК KINOMAX ПАРСЕРА")
        logger.info("=" * 80)
        
        kinomax_controller = KinomaxController()
        kinomax_controller.run(city="Липецк")
        
        logger.info("=" * 80)
        logger.info("KINOMAX ПАРСЕР ЗАВЕРШЁН")
        logger.info("=" * 80)
        
        logger.info("=" * 80)
        logger.info("ЗАПУСК MALIBU ПАРСЕРА")
        logger.info("=" * 80)
        
        malibu_controller = MalibuController()
        malibu_controller.run()
        
        logger.info("=" * 80)
        logger.info("MALIBU ПАРСЕР ЗАВЕРШЁН")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.exception(f"Ошибка при запуске парсера: {e}")
        return False
    
    return True

if __name__ == "__main__":
    setup_logging()
    
    # Очистка БД
    clear_database()
    
    # Запуск парсеров
    success = run_parsers()
    
    if success:
        logger.info("✓ Парсеры успешно завершены!")
    else:
        logger.error("✗ Парсеры завершены с ошибками")
