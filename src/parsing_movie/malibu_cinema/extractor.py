class MalibuMainPageExtractor:
    """Извлечение данных о фильмах Malibu"""

    def __init__(self, selectors: dict):
        self.selectors = selectors

    def parse_movie_card(self, element) -> dict[str, str]:
        """Парсинг карточки фильма на главной странице"""
        text = element.text.split('\n')

        title = text[0] if text else "Неизвестно"
        url = element.get_attribute('href')

        return {"title": title, "url": url}   


# class MalibuIdExtractor:
#     """Извлечение ID фильма из URL Малибу"""

#     @staticmethod
#     def extract(url: str) -> str | None:
#         if not url:
#             return None
#         parts = url.rstrip("/").split("/")
        
#         return parts[-1] if parts else None
