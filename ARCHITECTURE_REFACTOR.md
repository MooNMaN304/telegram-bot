# 🏗️ Архитектурный рефакторинг репозиториев

## 📋 Соответствие дизайну (BotDizain.drawio)

Текущая реализация полностью соответствует дизайну:

### 1. **Главная страница** ✅

- **Кнопка "Кинотеатры"** → `cinemas_list()` в handlers
  - Получает список всех кинотеатров
  - Показывает их с описанием (адрес)
  - Источник: `CinemaRepository.get_all()`

- **Кнопка "Дата"** → Функция на будущее (не реализована)
  - Позволит выбрать дату для фильтрации

### 2. **Меню Фильма** ✅

- Показывает информацию о выбранном фильме
- Отображает кинотеатры, где показывается фильм в выбранную дату
- Сеансы этого фильма в этих кинотеатрах
- Источник:
  - Информация: `MovieRepository.get_by_id()`
  - Кинотеатры: `CinemaMovieRepository.get_cinemas_by_movie_today()`

### 3. **Список Кинотеатров** ✅

- Получает список всех кинотеатров с кратким описанием
- При выборе кинотеатра показывает его фильмы на дату
- Источник:
  - Список: `CinemaRepository.get_all()`
  - Фильмы: `CinemaMovieRepository.get_movies_by_cinema_today()`

### 4. **Определённый Кинотеатр** ✅

- Показывает список фильмов в этом кинотеатре на дату
- Для каждого фильма показывает расписание (сеансы)
- Источник:
  - Фильмы: `CinemaMovieRepository.get_movies_by_cinema_today()`
  - Сеансы: `SessionRepository.get_by_movie_and_date()`

---

## 🔄 Как работает рефакторинг

### Раньше (❌ Неоптимально):

```
handlers.cinema_movies()
  ↓
MovieService.get_movies_by_cinema_today()
  ↓
1. MovieRepository.get_movies_by_cinema(cinema_id)  ← Получает ВСЕ фильмы
2. Затем для каждого фильма:
   SessionRepository.get_by_movie_and_date()  ← Фильтрует по сеансам
3. Фильтрует сеансы по cinema_id в Python коде (цикл)

❌ Проблемы:
- Дополнительный JOIN и фильтрация в Python
- N+1 query problem
```

### Теперь (✅ Оптимально):

```
handlers.cinema_movies()
  ↓
MovieService.get_movies_by_cinema_today(cinema_id)
  ↓
CinemaMovieRepository.get_movies_by_cinema_today(cinema_id)
  ↓
SELECT * FROM movies
  JOIN cinema_movies ON movies.id = cinema_movies.movie_id
  JOIN sessions ON movies.id = sessions.movie_id
  WHERE cinema_movies.cinema_id = ? AND DATE(sessions.date) = ?
  DISTINCT ON movies.id

✅ Преимущества:
- Один оптимизированный SQL запрос
- БД фильтрует данные (не Python)
- Избегаем N+1 problem
- Быстрее и меньше памяти
```

---

## 📂 Структура репозиториев

### MovieRepository (Фильмы)

```python
# Базовые CRUD операции
- get_all()                           # Все фильмы
- get_by_id(id)                       # Фильм по ID
- create(data)                        # Создать фильм
- update(id, data)                    # Обновить фильм
- delete(id)                          # Удалить фильм

# Поиск и фильтрация
- get_by_genre(genre)                 # По жанру
- search_by_name(name)                # Поиск по названию
- get_by_external_id(...)             # По внешнему ID (kinopoisk, malibu и т.д.)

# Связь с кинотеатрами
- get_or_create(name, cinema_id)      # Получить или создать с автосвязью
- _create_cinema_movie_relation()     # Создать связь с кинотеатром
- get_movies_by_cinema(cinema_id)     # DEPRECATED - используй CinemaMovieRepository

# Общие запросы
- get_movies_with_sessions_today()    # Фильмы, идущие сегодня
```

### CinemaMovieRepository (Связи Кинотеатр-Фильм) ⭐

```python
# Базовые операции со связями
- get_or_create(cinema_id, movie_id)              # Получить или создать
- get_by_cinema_and_movie(cinema_id, movie_id)    # Получить связь
- update(cinema_id, movie_id, data)               # Обновить
- delete(cinema_id, movie_id)                     # Удалить

# Оптимизированные запросы с JOIN (с поддержкой дат)
- get_movies_by_cinema(cinema_id)                 # Все фильмы в кинотеатре
- get_cinemas_by_movie(movie_id)                  # Все кинотеатры, где идёт фильм

- get_movies_by_cinema_today(cinema_id, date)     # ⭐ Фильмы на дату (с JOIN)
- get_cinemas_by_movie_today(movie_id, date)      # ⭐ Кинотеатры на дату (с JOIN)
```

### CinemaRepository (Кинотеатры)

```python
# Базовые CRUD операции
- get_all()                      # Все кинотеатры
- get_by_id(id)                  # По ID
- create(data)                   # Создать
- update(id, data)               # Обновить
- delete(id)                     # Удалить

# Поиск
- get_by_name(name)              # По названию
- get_or_create(data)            # Получить или создать
```

### SessionRepository (Сеансы)

```python
# Базовые CRUD операции
- get_all()                                   # Все сеансы
- get_by_id(id)                               # По ID
- create(data)                                # Создать
- update(id, data)                            # Обновить
- delete(id)                                  # Удалить

# Поиск и фильтрация
- get_by_session_id(session_id, cinema_id)   # По уникальному session_id
- get_by_movie(movie_id)                     # Все сеансы фильма
- get_by_movie_and_date(movie_id, date)      # Сеансы фильма на дату
- get_by_cinema_and_date(cinema_id, date)    # Сеансы кинотеатра на дату
- get_or_create(data)                        # Получить или создать
```

### UserRepository (Пользователи)

```python
# Базовые операции
- create(data)                              # Создать
- get_by_telegram_id(telegram_id)           # Получить пользователя
- update(telegram_id, data)                 # Обновить
```

---

## 🎯 Service Layer (MovieService)

```python
class MovieService:
    def __init__(self, movie_repo, session_repo, cinema_movie_repo):
        ...

    # Получение фильмов на сегодня
    def get_movies_with_sessions_today()
        # Использует: MovieRepository.get_movies_with_sessions_today()

    # Сеансы конкретного фильма на сегодня
    def get_sessions_for_movie_today(movie_id)
        # Использует: SessionRepository.get_by_movie_and_date()

    # ⭐ Фильмы в кинотеатре на дату (ОПТИМИЗИРОВАН)
    def get_movies_by_cinema_today(cinema_id, date=today)
        # Использует: CinemaMovieRepository.get_movies_by_cinema_today()
        # (С fallback на старый способ если cinema_movie_repo не передан)

    # ⭐ Кинотеатры, где идёт фильм на дату (ОПТИМИЗИРОВАН)
    def get_cinemas_by_movie_today(movie_id, date=today)
        # Использует: CinemaMovieRepository.get_cinemas_by_movie_today()
```

---

## 🎯 Handlers (Telegram Buttons)

```
/start
├─ Админ:
│  └─ "🚀 Запуск парсинга" → start_parsing()
│  └─ "🎬 Фильмы на сегодня" → films_today()
└─ Обычный пользователь:
   ├─ "🎬 Фильмы на сегодня" → films_today()
   │  └─ Выбор фильма → get_sessions_by_film()
   └─ "🏛 Кинотеатры" → cinemas_list()
      └─ Выбор кинотеатра → cinema_info()
         └─ "🎬 Фильмы в кинотеатре" → cinema_movies()
            └─ "🚪 Назад" → back_to_main()
```

---

## 📊 Diagrama данных

```
┌─────────────────────────────────────────────────────────────┐
│                        USERS                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ id | telegram_id | username | first_name | last_name │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        MOVIES                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ id | name | genre | description | poster | additional_data │
│  │    | (JSON с external IDs: kinopoisk_id, id_malibu)  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ (M:N)
                            │
                ┌──────────────────────────┐
                │  CINEMA_MOVIES (Link)    │
                │  ┌────────────────────┐  │
                │  │ cinema_id          │  │
                │  │ movie_id           │  │
                │  │ cinema_movie_id    │  │
                │  │ cinema_movie_url   │  │
                │  └────────────────────┘  │
                └──────────────────────────┘
                            ▲
                            │ (M:N)
                            │
┌─────────────────────────────────────────────────────────────┐
│                        CINEMAS                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ id | name | address | url | city | cinema_code | ... │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ (1:M)
                            │
┌─────────────────────────────────────────────────────────────┐
│                       SESSIONS                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ id | cinema_id | movie_id | date | time | session_id   │
│  │    | additional_data (JSON) | ...                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Оптимизационные улучшения

### Старая реализация проблемы:

```python
# ❌ MovieService.get_movies_by_cinema_today (старый способ)
all_cinema_movies = self.movie_repo.get_movies_by_cinema(cinema_id)  # Query 1
for movie in all_cinema_movies:
    sessions = self.session_repo.get_by_movie_and_date(movie.id, today)  # Query N
    cinema_sessions = [s for s in sessions if s.cinema_id == cinema_id]  # Python filter
```

### Новая реализация оптимизированной версии:

```python
# ✅ CinemaMovieRepository.get_movies_by_cinema_today (новый способ)
return (
    self.db.query(MovieModel)
    .join(CinemaMovieModel, MovieModel.id == CinemaMovieModel.movie_id)
    .join(SessionModel, MovieModel.id == SessionModel.movie_id)
    .filter(
        CinemaMovieModel.cinema_id == cinema_id,
        func.date(SessionModel.date) == target_date
    )
    .distinct(MovieModel.id)
    .all()
)
# ✅ Один оптимизированный SQL запрос!
```

---

## ✅ Checklist проверки

- [x] Репозитории разделены по смыслу (Movie, Cinema, CinemaMovie, Session, User)
- [x] CinemaMovie отвечает за связи и их фильтрацию
- [x] Методы с JOINами в cinema_movie_repository
- [x] Удалены дублирующиеся методы (или помечены как DEPRECATED)
- [x] Service layer использует оптимизированные методы
- [x] Handlers правильно используют сервисы
- [x] Архитектура соответствует дизайну (BotDizain.drawio)
- [x] Нет N+1 query проблем
- [x] Обработка ошибок в handlers
- [x] Логирование без дублирования
