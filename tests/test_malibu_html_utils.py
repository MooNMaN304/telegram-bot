"""
Тесты для HTML парсинга Malibu cinema.

Проверяют чистые функции извлечения данных без использования Selenium.
"""

import pytest
from pathlib import Path
from src.parsing_movie.malibu_cinema.html_utils import extract_release_links


@pytest.fixture
def malibu_with_movies_html() -> str:
    """HTML Malibu главной страницы с фильмами."""
    fixture_path = Path(__file__).parent / "html_parsing_tests" / "malibu_with_movies.html"
    if fixture_path.exists():
        return fixture_path.read_text(encoding="utf-8")
    return ""


@pytest.fixture
def malibu_without_movies_html() -> str:
    """HTML Malibu главной страницы без фильмов."""
    # Используем тот же фиксчур что и для тестов без сеансов
    fixture_path = Path(__file__).parent / "html_parsing_tests" / "malibu_without_movies.html"
    if fixture_path.exists():
        return fixture_path.read_text(encoding="utf-8")
    return ""


class TestExtractReleaseLinks:
    """Тесты извлечения ID релизов из HTML."""

    def test_extracts_release_links_from_container(self, malibu_with_movies_html):
        """Извлекает ID релизов из контейнера releases-container."""
        links = extract_release_links(malibu_with_movies_html)
        assert isinstance(links, list)
        assert len(links) > 0
        # Все элементы должны быть числами
        assert all(isinstance(link, str) and link.isdigit() for link in links)

    def test_extracts_unique_release_links(self, malibu_with_movies_html):
        """Гарантирует уникальность извлечённых ID."""
        links = extract_release_links(malibu_with_movies_html)
        assert len(links) == len(set(links)), "Есть дублирующиеся ID"

    def test_returns_empty_list_for_empty_html(self):
        """Возвращает пустой список для пустого HTML."""
        result = extract_release_links("")
        assert result == []

    def test_returns_empty_list_for_none(self):
        """Возвращает пустой список для None."""
        result = extract_release_links(None)
        assert result == []

    def test_handles_malformed_html(self):
        """Обрабатывает неправильный HTML без ошибок."""
        malformed = "<div><a href='/release/not_a_number'>Film</a></div>"
        result = extract_release_links(malformed)
        # Не должно быть ошибок, результат может быть пустым
        assert isinstance(result, list)

    def test_finds_links_anywhere_on_page(self):
        """Находит /release/ ссылки в любом месте страницы (не только в контейнере)."""
        html = "<div><a href='/release/123'>Film</a></div>"
        result = extract_release_links(html)
        assert result == ["123"]

    def test_returns_numeric_ids_only(self):
        """Фильтрует non-numeric ID (например 'soon')."""
        html = '''<div class="releases-list">
            <div class="releases-container">
                <a class="releases-item" href="/release/12345">Film 1</a>
                <a class="releases-item releases-item_soon" href="/release/soon">Coming Soon</a>
                <a class="releases-item" href="/release/67890">Film 2</a>
            </div>
        </div>'''
        result = extract_release_links(html)
        assert result == ["12345", "67890"]

    def test_handles_query_parameters_in_href(self):
        """Извлекает ID игнорируя query параметры."""
        html = '''<div class="releases-list">
            <div class="releases-container">
                <a class="releases-item" href="/release/12345/?sort=date">Film 1</a>
            </div>
        </div>'''
        result = extract_release_links(html)
        assert result == ["12345"]

    def test_maintains_order_of_appearance(self):
        """Сохраняет порядок появления ID."""
        html = '''<div class="releases-list">
            <div class="releases-container">
                <a class="releases-item" href="/release/333">Film 3</a>
                <a class="releases-item" href="/release/111">Film 1</a>
                <a class="releases-item" href="/release/222">Film 2</a>
            </div>
        </div>'''
        result = extract_release_links(html)
        assert result == ["333", "111", "222"]

    def test_approximately_19_films_in_fixture(self, malibu_with_movies_html):
        """В фиксчуре примерно 19 фильмов."""
        links = extract_release_links(malibu_with_movies_html)
        assert 15 <= len(links) <= 25  # Допустим диапазон


class TestIntegration:
    """Интеграционные тесты с реальными фиксчурами."""

    def test_with_real_malibu_fixture(self, malibu_with_movies_html):
        """Парсит реальную HTML Malibu без ошибок."""
        if not malibu_with_movies_html:
            pytest.skip("Фиксчур не найден")

        links = extract_release_links(malibu_with_movies_html)
        assert isinstance(links, list)
        assert len(links) > 0
        assert all(link.isdigit() for link in links)

    def test_without_movies_fixture(self, malibu_without_movies_html):
        """Обрабатывает страницу без фильмов без ошибок."""
        if not malibu_without_movies_html:
            pytest.skip("Фиксчур не найден")

        links = extract_release_links(malibu_without_movies_html)
        # Может быть пустой или содержать несколько элементов
        assert isinstance(links, list)
