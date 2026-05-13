# Архитектурные решения: Хранение Cinema-Specific данных

## Проблема

Раньше cinema-specific данные (ID фильма в кинотеатре, URL фильма на сайте кинотеатра) хранились в `MovieModel.additional_data` как JSON. Это было неправильно архитектурно, так как:

- Эти данные специфичны для конкретного кинотеатра, а не глобальны для фильма
- Усложняло логику получения данных
- Нарушало принцип нормализации БД

## Решение

Добавили cinema-specific поля в `CinemaMovieModel`:

### CinemaMovieModel

```python
class CinemaMovieModel(Base):
    __tablename__ = "cinema_movies"

    cinema_id = Column(Integer, ForeignKey("cinemas.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)

    # Cinema-specific данные ↓
    cinema_movie_id = Column(String(50), nullable=True)    # ID фильма в кинотеатре (напр. 24233 на Malibu)
    cinema_movie_url = Column(String(500), nullable=True)  # URL фильма на сайте кинотеатра
```

### Структура данных после изменений

**MovieModel.additional_data** (глобальные данные о фильме):

```json
{
  "name_en": "Predator: Descent",
  "duration": 120,
  "year": 2026,
  "rating": 8.5,
  "votes_count": 15000
}
```

**CinemaMovieModel** (связь фильм ↔ кинотеатр):

```
cinema_id: 1           # Малибу
movie_id: 5            # Хищник. Спуск в преисподнюю
cinema_movie_id: 24233 # ID на сайте Malibu
cinema_movie_url: "/release/24233?date=2026-04-08"  # URL на сайте
```

## Использование в парсере

### Сохранение фильма (контроллер)

```python
# 1. Сохраняем глобальный фильм (без cinema-specific данных)
movie = self.movie_repo.get_or_create(
    name=movie_details.title,
    cinema_id=malibu_cinema_id,
    defaults={
        "additional_data": movie_details.additional_data,  # глобальные данные
        ...
    },
)

# 2. Сохраняем связь фильм-кинотеатр с cinema-specific данными
cinema_movie = self.cinema_movie_repo.get_or_create(
    cinema_id=malibu_cinema_id,
    movie_id=movie.id,
    defaults={
        "cinema_movie_id": malibu_movie_id,      # cinema-specific
        "cinema_movie_url": malibu_url,          # cinema-specific
    },
)

# 3. Парсим сеансы используя cinema_movie_url
self.update_movie_sessions(cinema_movie, malibu_cinema_id)
```

### Получение данных (в будущем)

```python
# Получить все фильмы в кинотеатре с cinema-specific данными
cinema_movies = cinema_movie_repo.get_movies_by_cinema(cinema_id=1)
for cm in cinema_movies:
    print(f"Фильм: {cm.movie.name}")
    print(f"  ID в кинотеатре: {cm.cinema_movie_id}")
    print(f"  URL: {cm.cinema_movie_url}")
```

## Преимущества этого подхода

✅ **Нормализация БД** - cinema-specific данные в правильном месте  
✅ **Чистота данных** - `MovieModel` содержит только глобальные данные  
✅ **Масштабируемость** - легко добавить поддержку новых кинотеатров  
✅ **Производительность** - индексы на (cinema_id, movie_id)  
✅ **Семантика** - CinemaMovieModel явно представляет связь с данными

## Методы CinemaMovieRepository

```python
cinema_movie_repo.get_or_create(cinema_id, movie_id, defaults={...})
cinema_movie_repo.get_by_cinema_and_movie(cinema_id, movie_id)
cinema_movie_repo.get_movies_by_cinema(cinema_id)        # Все фильмы в кинотеатре
cinema_movie_repo.get_cinemas_by_movie(movie_id)         # Все кинотеатры, где идёт фильм
cinema_movie_repo.update(cinema_id, movie_id, data)
cinema_movie_repo.delete(cinema_id, movie_id)
```

## Миграция БД

Выполнить миграцию для добавления новых полей:

```bash
alembic upgrade head
```
