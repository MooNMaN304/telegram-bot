"""
Тесты для парсинга сеансов Malibu (session_extractor).

Проверяют извлечение данных из реального HTML используя Selenium Mock.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock
from lxml import html
from src.parsing_movie.malibu_cinema.session_extractor import MalibuSessionExtractor


@pytest.fixture
def selectors():
    """Стандартные селекторы из settings."""
    return {
        "schedule_block": ".release-schedule__items",
        "seance_item_xpath": ".//div[@data-seance-id]",
        "seance_parent_xpath": "./ancestor::div[contains(@class, 'seance-item')]",
    }


@pytest.fixture
def extractor(selectors):
    """Extractor с селекторами."""
    return MalibuSessionExtractor(selectors=selectors)


@pytest.fixture
def malibu_with_session_html() -> str:
    """HTML Malibu расписания с 3 сеансами."""
    fixture_path = Path(__file__).parent / "html_parsing_tests" / "malibu_with_session.html"
    if fixture_path.exists():
        return fixture_path.read_text(encoding="utf-8")
    return ""


@pytest.fixture
def malibu_without_session_html() -> str:
    """HTML Malibu расписания без сеансов."""
    fixture_path = Path(__file__).parent / "html_parsing_tests" / "malibu_without_session.html"
    if fixture_path.exists():
        return fixture_path.read_text(encoding="utf-8")
    return ""


def extract_seance_elements_from_html(html_str: str):
    """Парсит реальный HTML и возвращает mock Selenium элементы сеансов."""
    tree = html.fromstring(html_str)
    seance_elements = tree.xpath(".//div[@data-seance-id]")
    
    mocks = []
    for elem in seance_elements:
        mock = Mock()
        seance_id = elem.get("data-seance-id")
        mock.get_attribute.return_value = seance_id
        
        # Найти родительский seance-item - это нужно для find_element(By.XPATH, parent_xpath)
        parent = elem.getparent()
        while parent is not None and "seance-item" not in parent.get("class", ""):
            parent = parent.getparent()
        
        # Создаём mock родителя, который вернёт find_element
        if parent is not None:
            parent_text = parent.text_content().strip()
            parent_mock = Mock()
            parent_mock.text = parent_text  # Selenium WebElement.text свойство
        else:
            parent_mock = Mock()
            parent_mock.text = ""
        
        # Настраиваем find_element на возврат parent_mock
        # find_element(By.XPATH, "./ancestor::div[contains(@class, 'seance-item')]")
        from selenium.webdriver.common.by import By
        def mock_find_element(by, value):
            if "ancestor" in value and "seance-item" in value:
                return parent_mock
            raise Exception(f"XPath not found: {value}")
        
        mock.find_element = mock_find_element
        mocks.append(mock)
    
    return mocks


class TestMalibuSessionExtractorRealHTML:
    """Тесты с реальными фиксчурами HTML."""

    def test_extract_sessions_from_real_html_with_sessions(self, extractor, malibu_with_session_html):
        """Извлекает 3 сеанса из реального HTML с расписанием."""
        if not malibu_with_session_html:
            pytest.skip("Фиксчур malibu_with_session.html не найден")

        # Парсим реальный HTML и создаём Selenium mocks
        seance_mocks = extract_seance_elements_from_html(malibu_with_session_html)
        assert len(seance_mocks) == 3, f"Ожидалось 3 мока сеанса, получено {len(seance_mocks)}"
        
        # Создаём mock блока
        block = Mock()
        block.find_elements.return_value = seance_mocks

        sessions = extractor.parse_schedule_block(block)

        assert len(sessions) == 3, f"Ожидалось 3 сеанса, получено {len(sessions)}"
        
        # Проверяем что все сеансы имеют ID
        assert all(s["session_id"] for s in sessions), "Не все сеансы имеют ID"
        
        # Проверяем конкретные ID из фиксчура
        session_ids = [s["session_id"] for s in sessions]
        assert "69ddfc993c00004b00930d10" in session_ids
        assert "69ddfcbc3c00005100930d3b" in session_ids
        assert "69e0864d3f00009d006788af" in session_ids

    def test_extract_sessions_from_real_html_empty(self, extractor, malibu_without_session_html):
        """Возвращает пустой список для расписания без сеансов."""
        if not malibu_without_session_html:
            pytest.skip("Фиксчур malibu_without_session.html не найден")

        # Парсим реальный HTML и создаём Selenium mocks
        seance_mocks = extract_seance_elements_from_html(malibu_without_session_html)
        
        # Создаём mock блока
        block = Mock()
        block.find_elements.return_value = seance_mocks

        sessions = extractor.parse_schedule_block(block)
        
        # Если нет seance-id элементов - список пустой
        assert sessions == [], "Ожидается пустой список для расписания без сеансов"

    def test_extractor_initializes_with_selectors(self, selectors):
        """Extractor инициализируется со стандартными селекторами."""
        extractor = MalibuSessionExtractor(selectors=selectors)
        assert extractor.selectors == selectors

    def test_extractor_parse_none_returns_empty_list(self, extractor):
        """parse_schedule_block возвращает пустой список для None."""
        result = extractor.parse_schedule_block(None)
        assert isinstance(result, list)
        assert result == []


class TestSessionExtractorIntegration:
    """Интеграционные тесты с реальными фиксчурами."""

    def test_real_html_contains_three_seance_ids(self, malibu_with_session_html):
        """Фиксчур содержит 3 seance-id элемента."""
        if not malibu_with_session_html:
            pytest.skip("Фиксчур не найден")

        seance_ids = [
            "69ddfc993c00004b00930d10",
            "69ddfcbc3c00005100930d3b",
            "69e0864d3f00009d006788af"
        ]
        
        for seance_id in seance_ids:
            assert f'data-seance-id="{seance_id}"' in malibu_with_session_html, \
                f"seance_id {seance_id} не найден в фиксчуре"

    def test_real_html_contains_three_times(self, malibu_with_session_html):
        """Фиксчур содержит 3 времени сеансов."""
        if not malibu_with_session_html:
            pytest.skip("Фиксчур не найден")

        times = ["18:55", "20:45", "22:35"]
        
        for time_str in times:
            assert time_str in malibu_with_session_html, \
                f"Время {time_str} не найдено в фиксчуре"
