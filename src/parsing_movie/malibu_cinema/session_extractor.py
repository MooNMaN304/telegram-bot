from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import re
import logging

logger = logging.getLogger(__name__)


class MalibuSessionExtractor:
    """Extractor на основе устойчивых data-атрибутов.
    
    Работает ТОЛЬКО с селекторами из settings, не содержит логику XPath.
    """

    def __init__(self, selectors: dict):
        """
        Args:
            selectors: Словарь с селекторами из SESSION_SELECTORS["malibu"]
        """
        self.selectors = selectors

    def parse_schedule_block(self, block) -> list[dict]:
        """Парсит блок расписания, ищет сеансы по data-seance-id.
        
        Ранний выход если нет сеансов.
        
        Args:
            block: Selenium WebElement - контейнер с расписанием
            
        Returns:
            Список сеансов с полями: session_id, time, format, price
        """
        if not block:
            return []

        try:
            # ✅ ищем сразу по data-атрибуту через селектор из settings
            seances = block.find_elements(
                By.XPATH,
                self.selectors.get("seance_item_xpath", ".//div[@data-seance-id]")
            )
        except (NoSuchElementException, WebDriverException):
            return []

        # 🔥 ранний выход если нет сеансов
        if not seances:
            return []

        seances_data = []

        for seance in seances:
            try:
                # ✅ ID (главное)
                seance_id = seance.get_attribute("data-seance-id")
                if not seance_id:
                    continue

                # ⚠️ время и формат (может отсутствовать)
                seance_time = None
                format_text = None

                try:
                    parent_xpath = self.selectors.get(
                        "seance_parent_xpath",
                        "./ancestor::div[contains(@class, 'seance-item')]"
                    )
                    parent = seance.find_element(By.XPATH, parent_xpath)
                    text = parent.text.strip()

                    if text:
                        # попытка вытащить время из текста
                        match = re.search(r"\b\d{2}:\d{2}\b", text)
                        seance_time = match.group(0) if match else None
                        format_text = text

                except (NoSuchElementException, WebDriverException):
                    pass

                seances_data.append({
                    "session_id": seance_id,
                    "time": seance_time,
                    "format": format_text,
                    "price": None,
                })

            except (NoSuchElementException, WebDriverException, ValueError) as e:
                logger.warning("Ошибка при парсинге сеанса: %s", e)
                continue

        return seances_data

