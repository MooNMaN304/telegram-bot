"""
Утилиты для парсера Kinomax.
"""


def extract_kinomax_id(url: str) -> str:
    """
    Извлекает Kinomax ID из URL.
    
    Примеры:
        "https://kinomax.ru/films/9070/" -> "9070"
        "https://kinomax.ru/films/9070" -> "9070"
        "/films/9070?param=value" -> "9070"
    
    Args:
        url: URL на страницу фильма в Kinomax
    
    Returns:
        Kinomax ID (строка из цифр)
    """
    return url.rstrip("/").split("/")[-1].split("?")[0]
