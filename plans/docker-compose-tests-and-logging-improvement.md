# План: Тесты конфигурации и улучшение логирования

## Проблема

1. Парсеры не отрабатывают на продакшене, по логам непонятно почему
2. Нет автоматических тестов для проверки корректности docker-compose конфигурации

## Решение

### Часть 1: Тесты для docker-compose конфигурации

Создать файл `tests/test_docker_compose_config.py` с тестами:

#### 1.1 Проверка портов в docker-compose.frankfurt.yml

- [ ] postgres: должен иметь `ports: - "5432:5432"`
- [ ] redis: должен иметь `ports: - "6379:6379"`
- [ ] bot: не должен иметь проброшенных портов (только внутренние)

#### 1.2 Проверка портов в docker-compose.moscow.yml

- [ ] browserless: должен иметь `ports: - "3000:3000"`
- [ ] celery_worker: не должен иметь проброшенных портов

#### 1.3 Проверка environment variables

- [ ] В frankfurt bot должен иметь `DATABASE_URL` pointing to `postgres:5432`
- [ ] В moscow celery_worker должен иметь:
  - `DATABASE_URL` pointing to внешний IP Frankfurt:5432
  - `CELERY_BROKER_URL` pointing to `redis://redis:6379/0`
  - `CELERY_RESULT_BACKEND` pointing to `redis://redis:6379/0`
  - `REMOTE_SELENIUM_URL=http://browserless:3000/webdriver`

#### 1.4 Проверка networks

- [ ] Сервисы в frankfurt должны быть в `frankfurt_network`
- [ ] Сервисы в moscow должны быть в `moscow_network`
- [ ] Нет пересечений сетей между серверами

#### 1.5 Проверка depends_on и healthcheck

- [ ] bot зависит от postgres и redis с condition: service_healthy
- [ ] celery_worker зависит от browserless с condition: service_started

### Часть 2: Улучшение логирования

#### 2.1 Добавить структурированное логирование с контекстом

Создать middleware для добавления в логи:

- Имя сервиса (telegram-bot, celery-worker)
- Локацию сервера (frankfurt, moscow)
- ID задачи Celery (если есть)
- Время выполнения операций

#### 2.2 Детальные логи в парсерах

В `src/parsing_movie/celery.py`:

- [ ] Логировать начало и конец каждой задачи с временными метками
- [ ] Логировать параметры подключения при старте (без паролей)
- [ ] Логировать успешность подключения к БД и Redis

В `src/parsing_movie/kinomax_cinema/controller.py`:

- [ ] Добавить логирование перед открытием URL
- [ ] Логировать количество найденных фильмов
- [ ] Логировать успешность парсинга каждого фильма
- [ ] Логировать ошибки с полным stacktrace

В `src/parsing_movie/malibu_cinema/controller.py`:

- [ ] Аналогично добавить детальные логи
- [ ] Логировать процесс извлечения ID фильма
- [ ] Логировать статус обновления сеансов

#### 2.3 Улучшить celery.py для диагностики

- [ ] Добавить проверку подключения к БД перед запуском парсеров
- [ ] Добавить проверку подключения к Redis
- [ ] Добавить проверку доступности browserless (для malibu)
- [ ] Логировать результаты этих проверок

#### 2.4 Создать утилиту для "разбора" логов

Создать скрипт `scripts/analyze_logs.py` который:

- Парсит JSON логи из Loki/Promtail
- Группирует по service_name и server_location
- Показывает ошибки и warning'и
- Показывает timing операций

### Часть 3: Обновление GitHub Actions

#### 3.1 Добавить запуск тестов docker-compose

В `.github/workflows/main.yml`:

- [ ] Добавить шаг в job `test` для запуска `tests/test_docker_compose_config.py`
- [ ] Использовать `pytest -v tests/test_docker_compose_config.py`

#### 3.2 Добавить проверку валидности YAML

- [ ] Использовать `yamllint` или `docker compose config` для проверки синтаксиса

## Файлы для создания/изменения

### Новые файлы:

1. `tests/test_docker_compose_config.py` - тесты конфигурации
2. `scripts/analyze_logs.py` - скрипт анализа логов (опционально)

### Изменяемые файлы:

1. `src/parsing_movie/celery.py` - добавить диагностику подключений
2. `src/parsing_movie/kinomax_cinema/controller.py` - улучшить логи
3. `src/parsing_movie/malibu_cinema/controller.py` - улучшить логи
4. `.github/workflows/main.yml` - добавить тесты в CI

## Порядок выполнения

1. Создать тесты для docker-compose (быстро, можно запустить в CI)
2. Улучшить логирование в celery.py (диагностика подключений)
3. Улучшить логирование в контроллерах парсеров
4. Обновить GitHub Actions workflow
5. Протестировать на продакшене

## Ожидаемый результат

1. Тесты в CI гарантируют, что конфигурация docker-compose корректна
2. Детальные логи позволяют понять, на каком этапе падает парсер
3. Логи структурированы и легко фильтруются в Grafana/Loki
