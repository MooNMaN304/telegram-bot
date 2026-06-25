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
    Извлекает уникальные ID релизов со страницы.
    Без привязки к хэшированным CSS-классам — используем href-паттерн /release/.
    
    Args:
        page_html: HTML страницы сырой текст
        
    Returns:
        Список уникальных ID релизов в порядке появления (только числовые, без soon)
    """
    if not page_html or not isinstance(page_html, str):
        return []

    try:
        wrapped_html = f'<div>{page_html}</div>'
        tree = html.fromstring(wrapped_html)
    except Exception:
        return []

    # Ищем все ссылки с /release/
    links_xpath = malibu_settings.MAIN_PAGE_SELECTORS["movie_links_xpath"]
    links = tree.xpath(links_xpath)
    
    seen: Set[str] = set()
    result: List[str] = []
    
    for link in links:
        href = link.get("href", "")
        if not href:
            continue

        # Фильтруем "скоро" по тексту ссылки
        link_text = link.text_content().strip().lower()
        if 'soon' in link_text or 'скоро' in link_text:
            continue
            
        try:
            release_id = href.split("/release/")[1].split("?")[0].rstrip("/")
            if release_id.isdigit() and release_id not in seen:
                seen.add(release_id)
                result.append(release_id)
        except (IndexError, AttributeError):
            continue
    
    logger.info("Извлечено релизов: %d", len(result))
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
    Возвращает релизы с title + url + id.
    Без привязки к хэшированным CSS-классам — используем href-паттерны.
    """
    if not page_html:
        return []

    tree = html.fromstring(page_html)

    card_xpath = malibu_settings.HTML_UTILS_SELECTORS["release_cards"]["card_xpath"]
    release_path = malibu_settings.HTML_UTILS_SELECTORS["release_links"]["release_path"]
    
    # Находим все ссылки с /release/
    all_cards = tree.xpath(card_xpath)

    result = []
    seen_ids = set()

    for card in all_cards:
        href = card.get("href", "")
        if release_path not in href:
            continue

        try:
            release_id = href.split(release_path)[1].split("?")[0].strip("/")
        except (IndexError, AttributeError):
            continue

        # Фильтруем некорректные ID
        if not release_id or not release_id.isdigit() or release_id in seen_ids:
            continue

        # Фильтруем "скоро" — проверяем текст в нижнем регистре
        card_text_lower = card.text_content().strip().lower()
        if 'soon' in card_text_lower or 'скоро' in card_text_lower:
            continue

        seen_ids.add(release_id)

        # Извлекаем название из элемента releases-item-description__title
        # Если не найден — fallback на alt из img или href
        title = None
        title_divs = card.xpath(".//div[contains(@class, 'releases-item-description__title')]")
        if title_divs:
            title = title_divs[0].text_content().strip()

        # Fallback 1: <img alt="...">
        if not title:
            img = card.xpath(".//img[@data-name='poster']")
            if img:
                title = img[0].get("alt", "").strip()

        # Fallback 2: <img alt="Постер релиза"> — тогда берём href
        if not title:
            title = href  # хотя бы URL, потом kino-api подставит название

        base_url = malibu_settings.MALIBU_URL
        result.append({
            "release_id": release_id,
            "url": base_url + href,
            "title": title
        })

    logger.info("Извлечено релизов (без soon / ads): %d", len(result))
    return result