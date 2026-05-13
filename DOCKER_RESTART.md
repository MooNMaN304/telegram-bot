# Инструкция по перезапуску Docker контейнеров

## Проблемы, которые мы исправили:

1. **Ошибка 409 (несколько экземпляров бота)**
   - Заменили `restart: unless-stopped` на `restart: on-failure`
   - Добавили `max_retries: 3`
   - Это предотвращает бесконечный перезапуск и конфликты с Telegram API

2. **Отсутствие логов миграций**
   - Улучшили `entrypoint.bot.sh` с лучшей обработкой ошибок
   - Добавили проверку готовности PostgreSQL перед миграциями
   - Добавили информативные логи процесса

3. **Недостающий netcat**
   - Добавили `netcat-traditional` в `Dockerfile.bot` для проверки подключения к БД

## Как пересоздать контейнеры:

```bash
# 1. Остановить все контейнеры
docker-compose down -v

# 2. Удалить изображения (опционально, если хочешь чистый rebuild)
docker-compose down -v --rmi all

# 3. Перестроить изображения
docker-compose build --no-cache

# 4. Запустить контейнеры
docker-compose up -d

# 5. Проверить логи (в отдельном терминале)
docker-compose logs -f bot
docker-compose logs -f postgres
docker-compose logs -f celery_worker

# 6. Проверить что базы созданы в PgAdmin
# - Заходишь в http://localhost:5050 (если PgAdmin запущен)
# - Сервер: postgres:5432
# - Логин: cinema_user
# - Пароль: cinema_pass
# - База данных: cinema_db
```

## Если всё ещё не работает:

```bash
# Проверить статус контейнеров
docker-compose ps

# Посмотреть полные логи с ошибками
docker-compose logs --tail=100

# Проверить есть ли контейнер postgres и доступен ли он
docker exec cinema-postgres psql -U cinema_user -d cinema_db -c "\dt"

# Проверить что миграции применились
docker exec cinema-postgres psql -U cinema_user -d cinema_db -c "SELECT * FROM alembic_version;"
```

## Если БД не видна в PgAdmin:

1. Убедись что postgres контейнер healthy
2. Проверь логи postgres:
   ```bash
   docker-compose logs postgres
   ```
3. Проверь что пароль совпадает с .env файлом
4. Перезагрузи PgAdmin браузер (F5)

## Проверка что всё работает:

```bash
# 1. Должны быть таблицы в БД
docker exec cinema-postgres psql -U cinema_user -d cinema_db -c "\dt"

# 2. Результат должен быть:
#                List of relations
#  Schema |      Name      | Type  |     Owner
# --------+----------------+-------+-----------
#  public | alembic_version | table | cinema_user
#  public | cinema_movies  | table | cinema_user
#  public | cinemas        | table | cinema_user
#  public | movies         | table | cinema_user
#  public | sessions       | table | cinema_user
#  public | users          | table | cinema_user
```
