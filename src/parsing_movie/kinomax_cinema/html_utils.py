"""
Утилиты для работы с HTML страниц Kinomax.
Чистые функции без Selenium — легко тестировать через lxml.
"""
from lxml import html
import logging

from src.parsing_movie.kinomax_cinema.kinomax_settings import kinomax_settings

logger = logging.getLogger(__name__)


def has_empty_schedule_message(page_html: str) -> bool:
    """
    Проверяет, содержит ли страница сообщения о том, что сеансов нет.
    
    Args:
        page_html: Исходный HTML страницы
    
    Returns:
        True если найдено сообщение о пустом расписании
    """
    for message in kinomax_settings.EMPTY_SCHEDULE_MESSAGES:
        if message in page_html:
            logger.debug("Найдено сообщение о пустом расписании: %s", message)
            return True
    
    return False


def extract_order_links_html(page_html: str) -> str:
    """
    Извлекает только HTML ссылки с /order/ из страницы сеансов.
    Если страница содержит сообщения о пустом расписании, возвращает пустую строку.
    
    Args:
        page_html: Исходный HTML страницы (page_source из Selenium)
    
    Returns:
        Объединённый HTML всех найденных ссылок, или пустая строка если ничего не найдено
    
    Пример:
        >>> html_content = driver.page_source
        >>> order_links = extract_order_links_html(html_content)
        >>> assert "/order/" in order_links
    """
    try:
        # Сначала проверяем наличие сообщений о пустом расписании
        if has_empty_schedule_message(page_html):
            return ""
        
        tree = html.fromstring(page_html)
        nodes = tree.xpath("//a[contains(@href, '/order/')]")
        
        if not nodes:
            logger.debug("Ссылок с /order/ не найдено")
            return ""
        
        result_html = "\n".join([
            html.tostring(node, encoding="unicode")
            for node in nodes
        ])
        
        logger.debug("Извлечено %d ссылок, всего %d символов HTML", len(nodes), len(result_html))
        return result_html
        
    except Exception as e:  # noqa: BLE001
        logger.exception("Ошибка при парсинге HTML: %s", e)
        return ""


def _extract_title(node) -> str:
    """
    Извлекает название фильма из элемента используя цепочку fallback.
    
    Пытается получить title из:
    1. h4//span/text() — основной вариант
    2. h4/text() — альтернатива
    3. img/@alt — если нет h4
    
    Args:
        node: lxml Element узла ссылки на фильм
    
    Returns:
        Название фильма или пустая строка
    """
    xpaths = kinomax_settings.MAIN_PAGE_XPATHS

    # Пробуем получить title по приоритету
    candidates = (
        node.xpath(xpaths["title_primary"])
        or node.xpath(xpaths["title_fallback_1"])
        or node.xpath(xpaths["title_fallback_2"])
    )

    if not candidates:
        return ""

    return candidates[0].strip()


def extract_films_from_main(page_html: str) -> list[dict]:
    """
    Извлекает список фильмов со главной страницы Kinomax.
    
    Использует селекторы из KinomaxSettings для полной конфигурируемости.
    Парсит секцию с фильмами и ищет ссылки на /films/.
    Убирает дубликаты и фильтрует некорректные ID (должны быть числовыми).
    
    Args:
        page_html: HTML главной страницы (page_source из Selenium)
    
    Returns:
        Список словарей с ключами: id, url, title
        
    Пример:
        >>> films = extract_films_from_main(html_content)
        >>> assert len(films) > 0
        >>> assert all("id" in f for f in films)
    """
    try:
        tree = html.fromstring(page_html)

        # Получаем селекторы из settings
        section_xpath = kinomax_settings.MAIN_PAGE_XPATHS["movies_section"]
        links_xpath = kinomax_settings.MAIN_PAGE_XPATHS["movie_links"]

        # Ищем секцию с фильмами
        section = tree.xpath(section_xpath)
        if not section:
            logger.warning("Секция фильмов не найдена по селектору: %s", section_xpath)
            return []

        # Ищем ссылки на фильмы внутри этой секции
        nodes = section[0].xpath(links_xpath)

        if not nodes:
            logger.warning("Ссылки на фильмы не найдены")
            return []

        result = []
        seen_ids = set()

        for node in nodes:
            href = node.get("href", "")

            if "/films/" not in href:
                continue

            # Извлекаем ID фильма из URL: /films/9070/ -> 9070
            film_id = href.split("/films/")[-1].split("?")[0].strip("/")

            # Проверяем валидность ID
            if not film_id or film_id in seen_ids:
                continue

            # Фильтруем некорректные ID (должны быть числовыми, не "soon", "coming" и т.д.)
            if not film_id.isdigit():
                logger.debug("Пропускаем некорректный ID: %s", film_id)
                continue

            seen_ids.add(film_id)

            # 🔥 извлекаем название через универсальную функцию
            title = _extract_title(node)

            result.append({
                "id": film_id,
                "url": href,
                "title": title,
            })

        logger.info("Извлечено %d уникальных фильмов со главной страницы", len(result))
        return result

    except Exception as e:  # noqa: BLE001
        logger.exception("Ошибка при парсинге фильмов: %s", e)
        return []
