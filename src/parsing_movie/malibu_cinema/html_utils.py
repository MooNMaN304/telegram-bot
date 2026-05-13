"""
Утилиты чистого HTML парсинга для Malibu cinema.
Функции в этом модуле работают с HTML strings без использования Selenium.
"""

from lxml import html
from typing import List, Set
from urllib.parse import urlparse
from src.parsing_movie.malibu_cinema.malibu_settings import malibu_settings


def extract_release_links(page_html: str) -> List[str]:
    """
    Извлекает уникальные ссылки на релизы из основного контейнера.
    
    Args:
        page_html: HTML страницы сырой текст
        
    Returns:
        Список уникальных ID релизов в порядке появления
        
    Примеры:
        >>> html = '''<div class="releases-container">
        ...     <a href="/release/1234">Film 1</a>
        ...     <a href="/release/1234">Film 1</a>
        ... </div>'''
        >>> extract_release_links(html)
        ['1234']
    """
    if not page_html or not isinstance(page_html, str):
        return []

    try:
        tree = html.fromstring(page_html)
    except Exception:
        return []

    # Найти основной контейнер релизов
    container_xpath = malibu_settings.HTML_UTILS_SELECTORS["release_links"]["container_xpath"]
    container = tree.xpath(container_xpath)
    if not container:
        return []

    # Поиск ссылок ТОЛЬКО внутри контейнера
    link_xpath = malibu_settings.HTML_UTILS_SELECTORS["release_links"]["link_xpath"]
    links = container[0].xpath(link_xpath)
    
    seen: Set[str] = set()
    result: List[str] = []
    
    for link in links:
        href = link.get("href", "")
        if not href:
            continue
            
        # Извлечь ID из href: "/release/123456" -> "123456"
        release_path = malibu_settings.HTML_UTILS_SELECTORS["release_links"]["release_path"]
        try:
            release_id = href.split(release_path)[1].split("/")[0].split("?")[0]
            
            # Проверка что это цифры (исключаем "soon" и другие строки)
            if release_id.isdigit() and release_id not in seen:
                seen.add(release_id)
                result.append(release_id)
        except (IndexError, AttributeError):
            continue
    
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