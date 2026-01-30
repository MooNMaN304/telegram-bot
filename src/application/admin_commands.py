def run_parsing(service):
    try:
        service.malibu_movies_record()
    finally:
        service.main_parser.driver.quit()
        service.movie_repo.db.close()

    return "Парсинг завершён!"