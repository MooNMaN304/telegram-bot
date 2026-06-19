"""
Утилиты чистого HTML парсинга для Malibu cinema.
Функции в этом модуле работают с HTML strings без использования Selenium.
"""

from lxml import html
from typing import List, Set
from urllib.parse import urlparse
from src.parsing_movie.malibu_cinema.malibu_settings import malibu_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


def extract_release_links(page_html: str) -> List[str]:
    """
    Извлекает уникальные ссылки на релизы только из основного контейнера (без soon).
    
    Фильтрует:
    - Только releases-list контейнер (основной список фильмов)
    - Исключает releases-item_soon (скоро в кино)
    
    Args:
        page_html: HTML страницы сырой текст
        
    Returns:
        Список уникальных ID релизов в порядке появления
        
    Примеры:
        >>> html = '''<div class="releases-list">
        ...     <div class="releases-container">
        ...         <a class="releases-item" href="/release/1234">Film 1</a>
        ...         <a class="releases-item releases-item_soon" href="/release/5678">Soon</a>
        ...     </div>
        ... </div>'''
        >>> extract_release_links(html)
        ['1234']
    """
    if not page_html or not isinstance(page_html, str):
        return []

    try:
        # Оборачиваем в корневой элемент для корректного парсирования фрагментов
        wrapped_html = f'<div>{page_html}</div>'
        tree = html.fromstring(wrapped_html)
    except Exception:
        return []

    # ✅ Найти основной контейнер релизов (только releases-list, исключая soon)
    container_xpath = malibu_settings.MAIN_PAGE_SELECTORS["container_xpath"]
    container = tree.xpath(container_xpath)
    if not container:
        logger.warning("Контейнер releases-list не найден")
        return []

    # ✅ Поиск ссылок ТОЛЬКО активные (без soon)
    links_xpath = malibu_settings.MAIN_PAGE_SELECTORS["movie_links_xpath"]
    links = container[0].xpath(links_xpath)
    
    seen: Set[str] = set()
    result: List[str] = []
    
    for link in links:
        href = link.get("href", "")
        if not href:
            continue
            
        # Извлечь ID из href: "/release/123456" -> "123456" или "/release/123456/" -> "123456"
        try:
            release_id = href.split("/release/")[1].split("?")[0].rstrip("/")
            
            # Проверка что это цифры (исключаем другие строки)
            if release_id.isdigit() and release_id not in seen:
                seen.add(release_id)
                result.append(release_id)
        except (IndexError, AttributeError):
            continue
    
    logger.info("Отфильтровано релизов (без soon): %d", len(result))
    return result


def extract_film_title(page_html: str) -> str:
    """
    Извлекает название фильма из HTML с несколькими стратегиями fallback.
    
    Args:
        page_html: HTML страницы фильма
        
    Returns:
        Название фильма или пустая строка
    """
    if not page_html or not isinstance(page_html, str):
        return ""

    try:
        tree = html.fromstring(page_html)
    except Exception:
        return ""

    # Стратегия 1: Встроенный атрибут title в элементе
    h1_class = malibu_settings.HTML_UTILS_SELECTORS["film_title"]["h1_class"]
    title_elem = tree.xpath(f".//h1[@class='{h1_class}']")
    if title_elem:
        text = title_elem[0].text_content().strip()
        if text:
            return text

    # Стратегия 2: Любой h1 элемент
    general_h1_selector = malibu_settings.HTML_UTILS_SELECTORS["film_title"]["general_h1_selector"]
    h1_elements = tree.xpath(general_h1_selector)
    if h1_elements:
        text = h1_elements[0].text_content().strip()
        if text:
            return text

    # Стратегия 3: Meta og:title
    og_meta = malibu_settings.HTML_UTILS_SELECTORS["film_title"]["og_meta"]
    og_title = tree.xpath(f"//meta[@property='{og_meta}']/@content")
    if og_title:
        return og_title[0].strip()

    # Стратегия 4: title тег
    title_tag_selector = malibu_settings.HTML_UTILS_SELECTORS["film_title"]["title_tag_selector"]
    title_tag = tree.xpath(title_tag_selector)
    if title_tag:
        text = title_tag[0].strip()
        # Убрать " - кинотеатр Malibu" если есть
        title_suffix = malibu_settings.HTML_UTILS_SELECTORS["film_title"]["title_suffix"]
        if title_suffix in text:
            text = text.replace(title_suffix, "")
        return text

    return ""



def extract_release_cards(page_html: str) -> List[dict]:
    """
    Возвращает релизы с title + url + id
    """
    if not page_html:
        return []

    tree = html.fromstring(page_html)

    card_xpath = malibu_settings.HTML_UTILS_SELECTORS["release_cards"]["card_xpath"]
    release_path = malibu_settings.HTML_UTILS_SELECTORS["release_links"]["release_path"]
    
    # Исключаем блок "скоро" (releasesSoon)
    soon_id = malibu_settings.MAIN_PAGE_SELECTORS["soon_container_id"]
    soon_class = malibu_settings.MAIN_PAGE_SELECTORS["soon_class_part"]
    
    # Находим все карточки
    all_cards = tree.xpath(card_xpath)

    result = []

    for card in all_cards:
        # Проверка 1: Не находится ли карточка внутри контейнера "скоро"
        ancestors = card.xpath(f"ancestor::div[@id='{soon_id}']")
        if ancestors:
            continue
            
        # Проверка 2: Нет ли в классе самой карточки слова "soon"
        card_class = card.get("class", "")
        if soon_class in card_class:
            continue

        href = card.get("href", "")
        if release_path not in href:
            continue

        try:
            release_id = href.split(release_path)[1].split("?")[0]
        except:
            continue

        # 🔥 ВАЖНО: правильный селектор title
        title_class = malibu_settings.HTML_UTILS_SELECTORS["release_cards"]["title_class"]
        title_elem = card.xpath(f".//div[contains(@class,'{title_class}')]")

        title = title_elem[0].text_content().strip() if title_elem else None

        base_url = malibu_settings.MALIBU_URL
        result.append({
            "release_id": release_id,
            "url": base_url + href,
            "title": title
        })

    return result