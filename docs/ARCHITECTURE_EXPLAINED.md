# Архитектура проекта: как всё работает

## 1. Общая схема

```mermaid
graph TB
    subgraph "🌍 Сервер Франкфурт (Германия)"
        TG[Telegram Bot<br/>telegram_bot_app]
        PG[(PostgreSQL<br/>cinema-postgres)]
        RD[(Redis<br/>telegram_bot_redis)]
        LK[Loki - хранилище логов]
        GF[Grafana - веб-интерфейс логов]
        PT_F[Promtail - сборщик логов]

        TG -->|пишет данные| PG
        TG -->|очереди задач| RD
        TG -->|JSON-логи| PT_F
        PT_F -->|отправляет| LK
        LK -->|показывает| GF
    end

    subgraph "🌍 Сервер Москва (Россия)"
        BR[Browserless - браузер]
        CW[Celery Worker - парсер]
        PT_M[Promtail - сборщик логов]

        BR -->|открывает сайты| CW
        CW -->|JSON-логи| PT_M
        PT_M -->|отправляет по HTTP| LK
    end

    subgraph "☁️ GitHub"
        REPO[(GitHub Repository)]
        CI[GitHub Actions CI/CD]
    end

    TG <-->|получает команды| USER_Telegram_User
    CI -->|git push → авто-деплой| TG
    CI -->|git push → авто-деплой| CW
    USER_Telegram_User -->|выбирает фильм| TG
    TG -->|запускает задачу| RD
    RD -->|отдает задачу воркеру| CW
    CW -->|спарсенные данные| PG
```

## 2. Компоненты

### Логирование: Loki + Promtail + Grafana

| Компонент    | Что делает                                                                | Порт |
| ------------ | ------------------------------------------------------------------------- | ---- |
| **Loki**     | Хранит логи. Как база данных для логов, только легковесная                | 3100 |
| **Promtail** | Сидит на сервере, собирает логи из Docker контейнеров и отправляет в Loki | 9080 |
| **Grafana**  | Веб-интерфейс. Показывает логи из Loki в красивых дашбордах               | 3000 |

**Как логи путешествуют:**

```
Москва (воркер) → JSON-логи → Promtail → HTTP → Loki (Франкфурт) → Grafana (веб)
Франкфурт (бот) → JSON-логи → Promtail → Loki → Grafana (веб)
```

### CI/CD: GitHub Actions

Файл `.github/workflows/main.yml` — это инструкция для GitHub, что делать при каждом пуше:

1. **test** — запустить тесты Python на GitHub сервере
2. **deploy-frankfurt** — по SSH зайти на сервер → `git pull` → `docker compose up -d --build`
3. **deploy-moscow** — по SSH зайти на сервер → `git pull` → `docker compose up -d --build`

То есть **вы делаете git push, а GitHub сам деплоит на оба сервера**.

## 3. Как парсятся и передаются фильмы

```mermaid
sequenceDiagram
    User->>Bot: /start → "Запуск парсинга"
    Bot->>Redis: Создать задачу парсинга
    Redis->>Celery Worker (Москва): Отдать задачу
    Celery Worker->>Browserless: Открыть сайт кинотеатра
    Browserless->>Celery Worker: HTML страница
    Celery Worker->>Celery Worker: Распарсить фильмы и сеансы
    Celery Worker->>PostgreSQL (Франкфурт): Записать фильмы в БД
    Bot->>PostgreSQL: Прочитать фильмы из БД
    Bot->>User: Показать фильмы в Telegram
```

**Важно:** Воркер на Москве подключается к БД во Франкфурте **напрямую через интернет**. PostgreSQL во Франкфурте слушает порт 5432. Воркер использует `DATABASE_URL` с IP Франкфурта.

## 4. Ошибки на Москве и их решение

### Ошибка 1: `sqlalchemy.exc.ArgumentError`

```
Could not parse SQLAlchemy URL from given URL string
```

**Причина:** Переменная `DATABASE_URL` на московском сервере пуста или неверна.
Воркер пытается подключиться к БД во Франкфурте, но не знает адрес.

**Что нужно сделать:**
Зайдите по SSH на московский сервер и проверьте:

```bash
ssh ubuntu@MOSCOW_IP
cd /home/ubuntu/telegram-bot
cat .env | grep DATABASE_URL
```

Если строка пустая — нужно добавить секрет `MOSCOW_DATABASE_URL` в GitHub:

1. Зайдите на https://github.com/MooNMaN304/telegram-bot/settings/secrets/actions
2. Нажмите "New repository secret"
3. Name: `MOSCOW_DATABASE_URL`
4. Value: `postgresql+psycopg2://cinema_user:cinema_pass@31.76.96.6:5432/cinema_db`
5. Нажмите "Add secret"

После этого запушите любой коммит, и при деплое воркер получит правильный URL.

### Ошибка 2: Promtail - "entry too far behind"

```
entry with timestamp 2026-06-12 23:02:14 ignored, reason: 'entry too far behind'
```

Это **НЕ ОШИБКА**, а нормальное поведение. Когда воркер перезапускается много раз подряд, Promtail пытается отправить старые логи. Loki говорит: "эти логи слишком старые, я их не принимаю". Это не влияет на работу системы.

## 5. Где что смотреть в Grafana

1. **http://31.76.96.6:3000** — главная страница
2. **Explore (иконка лупы)** — ручной просмотр логов
   - В выпадающем списке выберите "Loki"
   - Нажмите "Run query" — увидете логи со всех серверов
3. **Dashboards (иконка квадратиков)** → **Bot Statistics** — готовый дашборд
4. **Слева → Containers** — выбрать конкретный контейнер:
   - `telegram_bot_app` — логи бота (Франкфурт)
   - `celery-worker` — логи воркера (Москва)
   - `promtail-moscow` — логи самого Promtail на Москве
