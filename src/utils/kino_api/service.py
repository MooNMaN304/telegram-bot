# from .client import KinoAPIClient


# class KinoMovieService:
#     def __init__(self):
#         self.client = KinoAPIClient()

#     def find_best_match(self, title: str):
#         """
#         Ищет фильм по названию.
#         Возвращает самый релевантный результат.
#         """
#         response = self.client.search_movie(title)

#         films = response.films
#         if not films:
#             return None

#         return films[0]

#     def get_movie_details(self, kp_id: int):
#         """
#         Возвращает подробную информацию о фильме
#         """
#         return self.client.get_film(kp_id)
