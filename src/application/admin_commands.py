def run_parsing(service):
    try:
        malibu_id = service.get_malibu_cinema_id()
        service.malibu_movies_record(malibu_id)
    finally:
        service.main_parser.driver.quit()
        service.db.close()

    return "Парсинг завершён!"  