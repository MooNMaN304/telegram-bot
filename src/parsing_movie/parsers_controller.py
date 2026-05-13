# TODO логика запуска парсеров -> celery tasks

from src.parsing_movie.abstract.controller import AbstractController
from src.parsing_movie.kinomax_cinema.controller import KinomaxController
from src.parsing_movie.malibu_cinema.controller import MalibuController


class ParsersController:
    """Класс котрый управляет всеми парсерами"""
    def __init__(self, parsers: list[AbstractController]):
        self.parsers = parsers
        
    def start(self):
        for parser in self.parsers:
            parser.run()
    