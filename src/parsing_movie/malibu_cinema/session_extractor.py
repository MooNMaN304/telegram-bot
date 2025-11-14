from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException


class MalibuSessionExtractor:
    """Извлечение данных о сеансах фильма (расписание) в кинотеатре Malibu"""

    def __init__(self, selectors: dict):
        self.selectors = selectors

    def parse_schedule_block(self, block) -> list[dict]:
        """Парсит один блок расписания (день)"""
        seances_data = []

        try:
            seances = block.find_elements(By.CSS_SELECTOR, self.selectors["seance_item"])
        except (NoSuchElementException, WebDriverException):
            return []

        for seance in seances:
            try:
                seance_id = seance.find_element(
                    By.CSS_SELECTOR, self.selectors["seance_id"]
                ).get_attribute("data-seance-id")

                time_el = seance.find_element(
                    By.CSS_SELECTOR, self.selectors["seance_time"]
                )
                seance_time = time_el.text.strip()

                desc_el = seance.find_element(By.CSS_SELECTOR, self.selectors["seance_description"])
                desc_lines = desc_el.text.split("\n")

                format_text = desc_lines[0] if len(desc_lines) > 0 else None
                price = desc_lines[1] if len(desc_lines) > 1 else None

                seances_data.append({
                    "session_id": seance_id,
                    "time": seance_time,
                    "format": format_text,
                    "price": price,
                })

            except (NoSuchElementException, WebDriverException):
                continue

        return seances_data