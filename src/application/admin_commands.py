from src.parsing_movie.celery import run_all_parsers_async

def run_parsing():
    try:
        ids = run_all_parsers_async()
        return ids
    except Exception as e:
        return f"Ошибка при запуске парсинга: {str(e)}"

