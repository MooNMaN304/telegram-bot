# Инструкция по разделенному деплою Telegram Movie Bot

## Архитектура

### Сервер во Франкфурте (Germany)
**Сервисы:**
- `bot` - Telegram бот
- `postgres` - база данных
- `redis` - брокер сообщений (защищен паролем)
- `vpn` - VPN соединение

**Почему здесь:**
- Telegram стабильнее работает вне РФ
- VPN уже находится здесь
- Postgres лучше не смешивать с Chromium

### Сервер в Москве (Russia)
**Сервисы:**
- `browserless` - headless Chrome для парсинга (1 сессия)
- `celery_worker` - воркеры для парсинга

**Почему здесь:**
- кинотеатры видят российский IP
- Chromium очень тяжелый по RAM
- browser automation лучше запускать отдельно

---

## Подготовка к деплою

### 1. Клонирование репозитория на оба сервера
```bash
git clone REPOSITORY_URL
cd telegram-bot
```

### 2. Настройка переменных окружения

#### На сервере во Франкфурте:
Скопируйте пример и отредактируйте:
```bash
cp .env.frankfurt.example .env
nano .env
```

**Что вписать в `.env` (Франкфурт):**
```env
# Токен Telegram бота (получить у @BotFather)
BOT_SECRET_KEY=ваш_токен_бота

# Ваш Telegram ID (узнать у @userinfobot)
ADMIN_TELEGRAM_ID=ваш_id

# API ключи
KINOPOISK_API_KEY=ваш_ключ_kinopoisk
GIGACHAT_API_KEY=ваш_ключ_gigachat

# Адрес browserless в Москве (замените на реальный IP Москвы)
REMOTE_SELENIUM_URL=http://IP_МОСКВЫ:3000/webdriver

# Redis с паролем (должен совпадать с docker-compose.frankfurt.yml)
CELERY_BROKER_URL=redis://:SUPER_SECRET_PASSWORD@redis:6379/0
CELERY_RESULT_BACKEND=redis://:SUPER_SECRET_PASSWORD@redis:6379/0

# База данных (локально)
DATABASE_URL=postgresql+psycopg2://cinema_user:cinema_pass@postgres:5432/cinema_db

# Логирование
LOG_LEVEL=INFO
```

#### На сервере в Москве:
Скопируйте пример и отредактируйте:
```bash
cp .env.moscow.example .env
nano .env
```

**Что вписать в `.env` (Москва):**
```env
# API ключи (нужны для парсинга)
KINOPOISK_API_KEY=ваш_ключ_kinopoisk
GIGACHAT_API_KEY=ваш_ключ_gigachat

# Redis на сервере во Франкфурте (замените на реальный IP Франкфурта)
REDIS_URL=redis://:SUPER_SECRET_PASSWORD@IP_ФРАНКФУРТА:6379/0
CELERY_BROKER_URL=${REDIS_URL}
CELERY_RESULT_BACKEND=${REDIS_URL}

# Browserless локально
REMOTE_SELENIUM_URL=http://browserless:3000/webdriver

# Логирование
LOG_LEVEL=INFO
```

---

## Настройка firewall

### На сервере во Франкфурте:
Открыть порт Redis (6379) **только для IP Москвы**:
```bash
# Пример для ufw (Ubuntu)
sudo ufw allow from IP_МОСКВЫ to any port 6379

# Пример для iptables
sudo iptables -A INPUT -p tcp -s IP_МОСКВЫ --dport 6379 -j ACCEPT
```

### На сервере в Москве:
Открыть порт Browserless (3000) **только для IP Франкфурта**:
```bash
# Пример для ufw (Ubuntu)
sudo ufw allow from IP_ФРАНКФУРТА to any port 3000

# Пример для iptables
sudo iptables -A INPUT -p tcp -s IP_ФРАНКФУРТА --dport 3000 -j ACCEPT
```

---

## Запуск сервисов

### На сервере во Франкфурте:
```bash
docker compose -f docker-compose.frankfurt.yml up -d --build
```

### На сервере в Москве:
```bash
# Обязательно создайте swap для Chromium!
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Запуск сервисов
docker compose -f docker-compose.moscow.yml up -d --build
```

---

## Важная архитектурная логика

### Celery worker в Москве:
**НЕ должен:**
- напрямую работать с postgres

**Должен:**
1. получить задачу через Redis (во Франкфурте)
2. спарсить сайт через browserless (локально)
3. вернуть результат через Redis

### Bot/Backend во Франкфурте:
**Должен:**
- получать результат из Redis
- записывать данные в postgres (локально)

---

## Преимущества такой схемы

### Безопасность
- Postgres не открыт наружу
- Redis защищен паролем
- Доступ между серверами ограничен по IP

### Производительность
- Нет постоянных запросов Москва → БД
- Chromium не конкурирует с Postgres за RAM
- Только Redis между серверами

---

## Полезные команды

### Проверка контейнеров
```bash
docker ps
```

### Логи (Франкфурт)
```bash
docker logs -f telegram_bot_app
docker logs -f cinema-postgres
docker logs -f telegram_bot_redis
```

### Логи (Москва)
```bash
docker logs -f telegram_bot_celery_worker
docker logs -f telegram_bot_browserless
```

### Мониторинг ресурсов
```bash
# Процессы и RAM
htop

# Docker статистика
docker stats

# Проверка RAM
free -h
```

### Обновление проекта (на обоих серверах)
```bash
git pull
docker compose -f docker-compose.[frankfurt|moscow].yml up -d --build
```

---

## Итоговая схема

### Frankfurt (Germany)
- Telegram bot
- Redis (пароль: SUPER_SECRET_PASSWORD)
- PostgreSQL
- VPN

### Moscow (Russia)
- Browserless (1 сессия)
- Celery worker

---

## Основная идея
Telegram + DB остаются в Германии.
Browser automation и парсинг работают из России.
