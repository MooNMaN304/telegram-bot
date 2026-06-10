# Настройка централизованного логирования

## Архитектура

```
Frankfurt Server                    Moscow Server
┌─────────────────────┐           ┌──────────────────────┐
│  Telegram Bot        │           │  Celery Worker        │
│  (JSON logs → stdout)│           │  (JSON logs → stdout) │
│         ↓            │           │         ↓             │
│  Promtail (docker)   │           │  Promtail (docker)   │
│         ↓            │           │         ↓             │
│  Loki (хранение)     │←──HTTP───│  (отправка логов)     │
│         ↓            │                                    │
│  Grafana (UI :3000)  │           └──────────────────────┘
└─────────────────────┘
```

## Компоненты

| Компонент | Версия | Назначение                       |
| --------- | ------ | -------------------------------- |
| Loki      | 2.9.2  | Хранение и индексация логов      |
| Promtail  | 2.9.2  | Сбор логов из Docker контейнеров |
| Grafana   | 10.2.3 | Визуализация и дашборды          |

## Запуск

### На сервере Франкфурта (Loki + Grafana + Promtail):

```bash
docker compose -f docker-compose.observability.yml up -d
```

### Доступ к Grafana:

- URL: `http://FRANKFURT_IP:3000`
- Логин: `admin`
- Пароль: `admin` (или задаётся через `GRAFANA_PASSWORD`)

## Дашборды

После запуска Grafana автоматически подгрузит дашборды из `observability/grafana/dashboards/`:

1. **Bot Statistics** (`bot-statistics.json`):
   - Логи по сервисам (Telegram Bot / Celery Worker)
   - Ошибки по сервисам
   - Логи по локациям (Frankfurt / Moscow)
   - Таймлайн действий пользователей
   - Статус задач парсинга

## Структура JSON-логов

```json
{
  "timestamp": "2026-06-10T19:20:00Z",
  "level": "INFO",
  "name": "src.main",
  "message": "Bot started",
  "service_name": "telegram-bot",
  "server_location": "frankfurt"
}
```

## Переменные окружения

| Переменная        | Описание                         | Пример                           |
| ----------------- | -------------------------------- | -------------------------------- |
| `SERVICE_NAME`    | Имя сервиса                      | `telegram-bot` / `celery-worker` |
| `SERVER_LOCATION` | Локация сервера                  | `frankfurt` / `moscow`           |
| `LOG_FORMAT`      | Формат логов (`json` или `text`) | `json`                           |
| `LOG_LEVEL`       | Уровень логирования              | `INFO` / `DEBUG`                 |

## Полезные LogQL запросы

```logql
# Все логи бота
{service_name="telegram-bot"}

# Ошибки воркера в Москве
{server_location="moscow", service_name="celery-worker"} |= "ERROR"

# Логи за последний час
{service_name=~"telegram-bot|celery-worker"} |= "parsing" | json

# Статистика ошибок по сервисам
sum(count_over_time({service_name=~"telegram-bot|celery-worker"} |= "ERROR" [$__range])) by (service_name)
```

## Безопасность

1. Порт 3100 (Loki) должен быть открыт только для сервера в Москве
2. Grafana рекомендуется защитить паролем (переменная `GRAFANA_PASSWORD`)
3. SSH ключи для деплоя хранить в GitHub Secrets
