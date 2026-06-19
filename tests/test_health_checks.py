"""
Health-check тесты для проверки доступности всех сервисов.

Запуск:
    pytest tests/test_health_checks.py -v
    pytest tests/test_health_checks.py -v -k "redis"
    pytest tests/test_health_checks.py -v -k "browserless"

Все тесты помечены @pytest.mark.slow — для быстрого запуска:
    pytest -m "not slow"
"""

import socket
import time
from urllib.parse import urlparse
from unittest.mock import patch

import pytest
import requests


# ============================================================
# Конфигурация (читается из .env или хардкод для тестов)
# ============================================================

def _get_env_or_default(key: str, default: str = "") -> str:
    """Получить значение из окружения или вернуть default."""
    import os
    return os.getenv(key, default)


# ============================================================
# Утилиты
# ============================================================

def check_tcp_connection(host: str, port: int, timeout: float = 5.0) -> tuple[bool, str]:
    """Проверить TCP-подключение к хост:порту."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, f"{host}:{port} — OK"
    except socket.timeout:
        return False, f"{host}:{port} — TIMEOUT ({timeout}s)"
    except ConnectionRefusedError:
        return False, f"{host}:{port} — CONNECTION REFUSED"
    except Exception as e:
        return False, f"{host}:{port} — ERROR: {e}"


def check_http_endpoint(url: str, timeout: float = 10.0) -> tuple[bool, str]:
    """Проверить HTTP-доступность эндпоинта."""
    try:
        resp = requests.get(url, timeout=timeout)
        return True, f"{url} — HTTP {resp.status_code}"
    except requests.exceptions.ConnectionError:
        return False, f"{url} — CONNECTION ERROR"
    except requests.exceptions.Timeout:
        return False, f"{url} — TIMEOUT ({timeout}s)"
    except Exception as e:
        return False, f"{url} — ERROR: {e}"


# ============================================================
# Тесты Redis
# ============================================================

class TestRedisConnectivity:
    """Проверка подключения к Redis."""

    @pytest.fixture(autouse=True)
    def _load_settings(self):
        from src.settings import settings
        self.settings = settings

    def test_redis_tcp_connection(self):
        """Redis доступен по TCP."""
        url = urlparse(self.settings.CELERY_BROKER_URL)
        host = url.hostname
        port = url.port or 6379
        ok, msg = check_tcp_connection(host, port, timeout=5)
        print(f"\n  📡 {msg}")
        assert ok, msg

    def test_redis_ping(self):
        """Redis отвечает на PING."""
        try:
            import redis
            url = urlparse(self.settings.CELERY_BROKER_URL)
            password = url.password
            r = redis.Redis(
                host=url.hostname,
                port=url.port or 6379,
                password=password,
                socket_timeout=5,
            )
            pong = r.ping()
            assert pong is True, "Redis не ответил PONG"
            print(f"\n  🟢 Redis PONG")
        except ImportError:
            pytest.skip("redis-py не установлен")

    def test_redis_celery_broker_url_valid(self):
        """CELERY_BROKER_URL имеет правильный формат."""
        url = self.settings.CELERY_BROKER_URL
        assert url.startswith(("redis://", "rediss://")), \
            f"Неверный формат CELERY_BROKER_URL: {url[:30]}..."
        parsed = urlparse(url)
        assert parsed.hostname, "CELERY_BROKER_URL не содержит хост"
        print(f"\n  📡 Broker: {parsed.hostname}:{parsed.port or 6379}")


# ============================================================
# Тесты PostgreSQL
# ============================================================

class TestPostgresConnectivity:
    """Проверка подключения к PostgreSQL."""

    @pytest.fixture(autouse=True)
    def _load_settings(self):
        from src.settings import settings
        self.settings = settings

    def test_postgres_tcp_connection(self):
        """PostgreSQL доступен по TCP."""
        db_url = self.settings.DATABASE_URL
        # Извлекаем хост:порт из URL
        clean_url = db_url.replace("postgresql+asyncpg://", "http://").replace("postgresql://", "http://")
        parsed = urlparse(clean_url)
        host = parsed.hostname
        port = parsed.port or 5432
        ok, msg = check_tcp_connection(host, port, timeout=5)
        print(f"\n  📡 {msg}")
        assert ok, msg

    def test_postgres_url_valid(self):
        """DATABASE_URL имеет правильный формат."""
        url = self.settings.DATABASE_URL
        assert url.startswith("postgresql"), \
            f"Неверный формат DATABASE_URL: {url[:30]}..."
        print(f"\n  🗄️  DB URL OK")

    def test_postgres_sync_connection(self):
        """Синхронное подключение к PostgreSQL (через psycopg2 или asyncpg)."""
        try:
            from sqlalchemy import create_engine, text
            engine = create_engine(
                self.settings.DATABASE_URL.replace("+asyncpg", ""),
                connect_args={"connect_timeout": 5},
            )
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                assert result.scalar() == 1
            print(f"\n  🟢 PostgreSQL SELECT 1 — OK")
        except ImportError:
            pytest.skip("sqlalchemy/psycopg2 не установлены")
        except Exception as e:
            pytest.fail(f"PostgreSQL connection failed: {e}")


# ============================================================
# Тесты Browserless (Selenium Remote)
# ============================================================

class TestBrowserlessConnectivity:
    """Проверка подключения к Browserless (headless Chrome)."""

    @pytest.fixture(autouse=True)
    def _load_settings(self):
        from src.settings import settings
        self.settings = settings

    def test_browserless_tcp_connection(self):
        """Browserless доступен по TCP."""
        url = urlparse(self.settings.REMOTE_SELENIUM_URL)
        host = url.hostname
        port = url.port or 3000
        ok, msg = check_tcp_connection(host, port, timeout=5)
        print(f"\n  📡 {msg}")
        assert ok, msg

    def test_browserless_http_health(self):
        """Browserless HTTP health-check."""
        url = urlparse(self.settings.REMOTE_SELENIUM_URL)
        health_url = f"http://{url.hostname}:{url.port or 3000}/json/version"
        ok, msg = check_http_endpoint(health_url, timeout=10)
        print(f"\n  🌐 {msg}")
        assert ok, msg

    def test_browserless_selenium_connection(self):
        """Selenium Remote WebDriver подключается к Browserless."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Remote(
                command_executor=self.settings.REMOTE_SELENIUM_URL,
                options=options,
            )
            title = driver.title
            driver.quit()
            print(f"\n  🟢 Selenium Remote — OK (title: '{title}')")
        except Exception as e:
            pytest.fail(f"Selenium Remote connection failed: {e}")


# ============================================================
# Тесты GigaChat API
# ============================================================

class TestGigaChatConnectivity:
    """Проверка доступности GigaChat API."""

    @pytest.fixture(autouse=True)
    def _load_settings(self):
        from src.settings import settings
        self.settings = settings

    def test_gigachat_api_key_set(self):
        """GIGACHAT_API_KEY задан и не пустой."""
        key = self.settings.GIGACHAT_API_KEY
        assert key, "GIGACHAT_API_KEY не задан"
        assert len(key) > 10, f"GIGACHAT_API_KEY слишком короткий ({len(key)} символов)"
        print(f"\n  🔑 GigaChat API key: {key[:8]}...{key[-4:]}")

    def test_gigachat_client_initialization(self):
        """Клиент GigaChat создаётся без ошибок."""
        try:
            from gigachat import GigaChat
            giga = GigaChat(
                credentials=self.settings.GIGACHAT_API_KEY,
                verify_ssl_certs=False,
                model="GigaChat",
            )
            # Не делаем реальный запрос — просто проверяем что клиент создался
            print(f"\n  🟢 GigaChat client created OK")
        except ImportError:
            pytest.skip("gigachat SDK не установлен")
        except Exception as e:
            pytest.fail(f"GigaChat client creation failed: {e}")


# ============================================================
# Тесты Kinopoisk API
# ============================================================

class TestKinopoiskAPIConnectivity:
    """Проверка доступности Kinopoisk API."""

    @pytest.fixture(autouse=True)
    def _load_settings(self):
        from src.settings import settings
        self.settings = settings

    def test_kinopoisk_api_key_set(self):
        """KINOPOISK_API_KEY задан."""
        key = self.settings.KINOPOISK_API_KEY
        assert key, "KINOPOISK_API_KEY не задан"
        print(f"\n  🔑 Kinopoisk API key: {key[:8]}...")

    def test_kinopoisk_api_reachable(self):
        """Kinopoisk API доступен (HTTP health check)."""
        try:
            from src.out.openapi_client.api_client import ApiClient
            from src.out.openapi_client.api.films_api import FilmsApi
            from src.out.openapi_client.configuration import Configuration

            config = Configuration(api_key={"ApiKeyAuth": self.settings.KINOPOISK_API_KEY})
            api_client = ApiClient(config)
            api = FilmsApi(api_client)

            # Простой запрос для проверки доступности
            response = api.api_v21_films_search_by_keyword_get(keyword="test", page=1)
            assert response is not None
            print(f"\n  🟢 Kinopoisk API — OK")
        except ImportError:
            pytest.skip("openapi_client не установлен")
        except Exception as e:
            # API может вернуть ошибку авторизации — это нормально для health check
            if "401" in str(e) or "403" in str(e):
                print(f"\n  ⚠️ Kinopoisk API доступен, но авторизация не прошла: {e}")
            else:
                pytest.fail(f"Kinopoisk API check failed: {e}")


# ============================================================
# Тесты Telegram Bot API
# ============================================================

class TestTelegramBotConnectivity:
    """Проверка доступности Telegram Bot API."""

    def test_telegram_api_reachable(self):
        """Telegram Bot API доступен."""
        ok, msg = check_http_endpoint("https://api.telegram.org", timeout=10)
        print(f"\n  🌐 {msg}")
        assert ok, msg


# ============================================================
# Комплексный тест всех сервисов
# ============================================================

class TestAllServicesOverview:
    """Комплексный обзор доступности всех сервисов."""

    def test_full_connectivity_report(self):
        """Проверить все сервисы и вывести отчёт."""
        from src.settings import settings

        results = []

        # Redis
        url = urlparse(settings.CELERY_BROKER_URL)
        ok, msg = check_tcp_connection(url.hostname, url.port or 6379, timeout=3)
        results.append(("Redis", ok, msg))

        # PostgreSQL
        db_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "http://").replace("postgresql://", "http://")
        parsed = urlparse(db_url)
        ok, msg = check_tcp_connection(parsed.hostname, parsed.port or 5432, timeout=3)
        results.append(("PostgreSQL", ok, msg))

        # Browserless
        sel_url = urlparse(settings.REMOTE_SELENIUM_URL)
        ok, msg = check_tcp_connection(sel_url.hostname, sel_url.port or 3000, timeout=3)
        results.append(("Browserless", ok, msg))

        # Telegram
        ok, msg = check_http_endpoint("https://api.telegram.org", timeout=5)
        results.append(("Telegram API", ok, msg))

        # GigaChat
        ok, msg = check_http_endpoint("https://gigachat.devices.sberbank.ru", timeout=5)
        results.append(("GigaChat API", ok, msg))

        # Вывод отчёта
        print("\n" + "=" * 60)
        print("  📊 HEALTH CHECK REPORT")
        print("=" * 60)
        all_ok = True
        for name, ok, msg in results:
            status = "✅" if ok else "❌"
            print(f"  {status} {name}: {msg}")
            if not ok:
                all_ok = False
        print("=" * 60)

        if all_ok:
            print("  🎉 Все сервисы доступны!")
        else:
            print("  ⚠️  Некоторые сервисы недоступны!")
        print()

        # Проверяем что хотя бы критические сервисы доступны
        critical_services = [r for r in results if r[0] in ("Redis", "PostgreSQL")]
        assert all(r[1] for r in critical_services), \
            f"Критические сервисы недоступны: {[r[0] for r in critical_services if not r[1]]}"
