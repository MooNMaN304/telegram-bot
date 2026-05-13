"""
Тесты для html_utils.py — парсинга HTML через lxml.
Этот уровень НЕ завязан на Selenium, только на lxml.
"""
from pathlib import Path
import pytest
from lxml import html

from src.parsing_movie.kinomax_cinema.html_utils import (
    extract_order_links_html,
    has_empty_schedule_message,
    extract_films_from_main,
    _extract_title,
)


class TestExtractOrderLinksHtml:
    """Тесты для extract_order_links_html — чистая функция"""

    @pytest.fixture
    def html_with_sessions(self) -> str:
        """HTML с сеансами (есть /order/ ссылки) — реальная фиксчура"""
        html_file = Path(__file__).parent / "html_parsing_tests" / "with_session.html"
        return html_file.read_text(encoding="utf-8")

    @pytest.fixture
    def html_without_sessions(self) -> str:
        """HTML без сеансов (нет /order/ ссылок) — реальная фиксчура"""
        html_file = Path(__file__).parent / "html_parsing_tests" / "without_session.html"
        return html_file.read_text(encoding="utf-8")

    def test_extract_with_sessions(self, html_with_sessions: str) -> None:
        """Должны найтись все ссылки /order/"""
        result = extract_order_links_html(html_with_sessions)

        # Проверяем, что найдены все нужные ID заказов (из with_session.html)
        expected_orders = [
            "/order/3552581",
            "/order/3552582",
            "/order/3552583",
            "/order/3552584",
            "/order/3552585",
        ]
        
        for order_id in expected_orders:
            assert order_id in result, f"Не найден {order_id} в результате"
        
        # Результат не пуст
        assert result != ""
        
        # HTML валиден (содержит <a href)
        assert "href" in result
        assert "<a" in result

    def test_extract_without_sessions(self, html_without_sessions: str) -> None:
        """
        Тест с without_session.html — нет /order/ ссылок
        (это страница, где сеансы действительно отсутствуют)
        """
        result = extract_order_links_html(html_without_sessions)

        # Файл не содержит /order/ ссылок
        assert result == ""

    def test_extract_empty_html(self) -> None:
        """Пустой HTML вернёт пустую строку"""
        result = extract_order_links_html("")

        assert result == ""

    def test_extract_malformed_html(self) -> None:
        """Некорректный HTML обработается без исключения"""
        malformed = "<div><a href='/order/123'>"  # Не закрыто
        result = extract_order_links_html(malformed)

        # Функция должна справиться и вернуть результат
        # lxml парсит даже сломанный HTML
        assert "/order/123" in result or result == ""
        
    def test_extract_multiple_order_links_order(self, html_with_sessions: str) -> None:
        """Ссылки должны быть в порядке появления в HTML"""
        result = extract_order_links_html(html_with_sessions)

        # Порядок должен быть: 3552581 -> 3552582 -> 3552583 -> 3552584 -> 3552585
        pos_3552581 = result.find("/order/3552581")
        pos_3552585 = result.find("/order/3552585")
        
        assert pos_3552581 != -1
        assert pos_3552585 != -1
        assert pos_3552581 < pos_3552585


class TestHasEmptyScheduleMessage:
    """Тесты для has_empty_schedule_message"""

    def test_detect_schedule_not_found(self) -> None:
        """Должна найтись фраза 'Сеансы не найдены'"""
        html_with_message = "<div>Сеансы не найдены</div>"
        
        result = has_empty_schedule_message(html_with_message)
        
        assert result is True

    def test_detect_schedule_being_compiled(self) -> None:
        """Должна найтись фраза 'Расписание составляется'"""
        html_with_message = "<div>Расписание составляется...</div>"
        
        result = has_empty_schedule_message(html_with_message)
        
        assert result is True

    def test_no_empty_message(self) -> None:
        """Если нет сообщений, должно вернуться False"""
        html_without_message = "<div><a href='/order/123'>Заказать</a></div>"
        
        result = has_empty_schedule_message(html_without_message)
        
        assert result is False

    def test_extract_skips_empty_schedule_pages(self) -> None:
        """extract_order_links_html должна вернуть пусто, если есть сообщение о пустом расписании"""
        html_with_empty_message = (
            "<div>Расписание составляется</div>"
            "<a href='/order/123'>Заказать</a>"  # Эта ссылка не должна быть извлечена
        )
        
        result = extract_order_links_html(html_with_empty_message)
        
        # Несмотря на наличие /order/, результат пуст
        assert result == ""


class TestExtractTitle:
    """Тесты для _extract_title — извлечение названия фильма"""

    def test_extract_title_primary(self) -> None:
        """Должно извлечь title из h4//span/text()"""
        html_content = """
        <a href="/films/1234/">
            <h4><span>Фильм 1</span></h4>
        </a>
        """
        node = html.fromstring(html_content)
        result = _extract_title(node)
        
        assert result == "Фильм 1"

    def test_extract_title_fallback_1(self) -> None:
        """Должно извлечь title из h4/text() если нет span"""
        html_content = """
        <a href="/films/1234/">
            <h4>Фильм 2</h4>
        </a>
        """
        node = html.fromstring(html_content)
        result = _extract_title(node)
        
        assert result == "Фильм 2"

    def test_extract_title_fallback_2(self) -> None:
        """Должно извлечь title из img/@alt если нет h4"""
        html_content = """
        <a href="/films/1234/">
            <img alt="Фильм 3"/>
        </a>
        """
        node = html.fromstring(html_content)
        result = _extract_title(node)
        
        assert result == "Фильм 3"

    def test_extract_title_empty(self) -> None:
        """Должно вернуть пустую строку если ничего не найдено"""
        html_content = """
        <a href="/films/1234/">
            <div>Без названия</div>
        </a>
        """
        node = html.fromstring(html_content)
        result = _extract_title(node)
        
        assert result == ""

    def test_extract_title_with_whitespace(self) -> None:
        """Должно обрезать лишние пробелы"""
        html_content = """
        <a href="/films/1234/">
            <h4><span>  Фильм с пробелами  </span></h4>
        </a>
        """
        node = html.fromstring(html_content)
        result = _extract_title(node)
        
        assert result == "Фильм с пробелами"


class TestExtractFilmsFromMain:
    """Тесты для extract_films_from_main — извлечение фильмов со главной"""

    @pytest.fixture
    def html_main_with_movies(self) -> str:
        """HTML главной страницы с фильмами — реальная фиксчура"""
        html_file = Path(__file__).parent / "html_parsing_tests" / "main_with_movies.html"
        return html_file.read_text(encoding="utf-8")

    def test_extract_films_returns_list(self, html_main_with_movies: str) -> None:
        """Должен вернуться список фильмов"""
        result = extract_films_from_main(html_main_with_movies)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_extract_films_has_required_fields(self, html_main_with_movies: str) -> None:
        """Каждый фильм должен иметь id, url, title"""
        result = extract_films_from_main(html_main_with_movies)

        for film in result:
            assert "id" in film
            assert "url" in film
            assert "title" in film
            assert film["id"] != ""

    def test_extract_films_correct_count(self, html_main_with_movies: str) -> None:
        """Должно быть ~20 фильмов (уникальные)"""
        result = extract_films_from_main(html_main_with_movies)

        # Проверяем, что количество разумное (20-50 фильмов)
        assert 15 < len(result) < 50, f"Ожидалось ~20 фильмов, получено {len(result)}"

    def test_extract_films_unique_ids(self, html_main_with_movies: str) -> None:
        """Все ID должны быть уникальными (нет дубликатов)"""
        result = extract_films_from_main(html_main_with_movies)

        ids = [film["id"] for film in result]
        
        assert len(ids) == len(set(ids)), f"Найдены дубликаты! IDs: {ids}"

    def test_extract_films_correct_format(self, html_main_with_movies: str) -> None:
        """URL должны содержать /films/, ID должны быть числами"""
        result = extract_films_from_main(html_main_with_movies)

        for film in result:
            # URL должен содержать /films/
            assert "/films/" in film["url"]
            
            # ID должен быть числом или строкой из цифр
            assert film["id"].isdigit(), f"ID должен быть числом, получено: {film['id']}"

    def test_extract_empty_html(self) -> None:
        """Пустой HTML должен вернуть пустой список"""
        result = extract_films_from_main("")

        assert result == []

    def test_extract_malformed_html(self) -> None:
        """Некорректный HTML обработается без исключения"""
        malformed = "<section><a href='/films/123'>Film</a>"  # Не закрыто
        result = extract_films_from_main(malformed)

        # Функция должна справиться и вернуть результат или пустой список
        assert isinstance(result, list)
