"""
Health-check тесты для проверки доступности всех сервисов.

Запуск:
    pytest tests/test_health_checks.py -v
    pytest tests/test_health_checks.py -v -k "redis"
    pytest tests/test_health_checks.py -v -k "browserless"
    pytest tests/test_health_checks.py -v -k "full"

ВАЖНО: Эти тесты используют os.getenv() напрямую, а НЕ src.settings,
чтобы не падать в CI/CD где обязательные env vars не заданы.
Если переменная не задана — тест пропускается (skip).
"""

import os
import socket
from urllib.parse import urlparse

import pytest


# ============================================================
# Утилиты
# ============================================================

def _get_env(key: str) -> str | None:
    """Получить значение из окружения. None если не задано."""
    return os.getenv(key) or None


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
        import requests
        resp = requests.get(url, timeout=timeout)
        return True, f"{url} — HTTP {resp.status_code}"
    except ImportError:
        return False, f"{url} — requests не установлен"
    except Exception as e:
        return False, f"{url} — ERROR: {e}"


# ============================================================
# Тесты Redis
# ============================================================

class TestRedisConnectivity:
    """Проверка подключения к Redis."""

    def test_redis_tcp_connection(self):
        """Redis доступен по TCP."""
        broker_url = _get_env("CELERY_BROKER_URL")
        if not broker_url:
            pytest.skip("CELERY_BROKER_URL не задан")

        url = urlparse(broker_url)
        host = url.hostname
        port = url.port or 6379
        ok, msg = check_tcp_connection(host, port, timeout=5)
        print(f"\n  📡 {msg}")
        assert ok, msg

    def test_redis_ping(self):
        """Redis отвечает на PING."""
        broker_url = _get_env("CELERY_BROKER_URL")
        if not broker_url:
            pytest.skip("CELERY_BROKER_URL не задан")

        try:
            import redis
            url = urlparse(broker_url)
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

    def test_redis_broker_url_valid(self):
        """CELERY_BROKER_URL имеет правильный формат."""
        broker_url = _get_env("CELERY_BROKER_URL")
        if not broker_url:
            pytest.skip("CELERY_BROKER_URL не задан")

        assert broker_url.startswith(("redis://", "rediss://")), \
            f"Неверный формат CELERY_BROKER_URL: {broker_url[:30]}..."
        parsed = urlparse(broker_url)
        assert parsed.hostname, "CELERY_BROKER_URL не содержит хост"
        print(f"\n  📡 Broker: {parsed.hostname}:{parsed.port or 6379}")


# ============================================================
# Тесты PostgreSQL
# ============================================================

class TestPostgresConnectivity:
    """Проверка подключения к PostgreSQL."""

    def test_postgres_tcp_connection(self):
        """PostgreSQL доступен по TCP."""
        db_url = _get_env("DATABASE_URL")
        if not db_url:
            pytest.skip("DATABASE_URL не задан")

        clean_url = db_url.replace("postgresql+asyncpg://", "http://").replace("postgresql://", "http://")
        parsed = urlparse(clean_url)
        host = parsed.hostname
        port = parsed.port or 5432
        ok, msg = check_tcp_connection(host, port, timeout=5)
        print(f"\n  📡 {msg}")
        assert ok, msg

    def test_postgres_url_valid(self):
        """DATABASE_URL имеет правильный формат."""
        db_url = _get_env("DATABASE_URL")
        if not db_url:
            pytest.skip("DATABASE_URL не задан")

        assert db_url.startswith("postgresql"), \
            f"Неверный формат DATABASE_URL: {db_url[:30]}..."
        print(f"\n  🗄️  DB URL OK")

    def test_postgres_sync_connection(self):
        """Синхронное подключение к PostgreSQL."""
        db_url = _get_env("DATABASE_URL")
        if not db_url:
            pytest.skip("DATABASE_URL не задан")

        try:
            from sqlalchemy import create_engine, text
            engine = create_engine(
                db_url.replace("+asyncpg", ""),
                connect_args={"connect_timeout": 5},
            )
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                assert result.scalar() == 1
            print(f"\n  🟢 PostgreSQL SELECT 1 — OK")
        except ImportError:
            pytest.skip("sqlalchemy не установлен")
        except Exception as e:
            pytest.fail(f"PostgreSQL connection failed: {e}")


# ============================================================
# Тесты Browserless (Selenium Remote)
# ============================================================

class TestBrowserlessConnectivity:
    """Проверка подключения к Browserless (headless Chrome)."""

    def test_browserless_tcp_connection(self):
        """Browserless доступен по TCP."""
        sel_url_str = _get_env("REMOTE_SELENIUM_URL")
        if not sel_url_str:
            pytest.skip("REMOTE_SELENIUM_URL не задан")

        url = urlparse(sel_url_str)
        host = url.hostname
        port = url.port or 3000
        ok, msg = check_tcp_connection(host, port, timeout=5)
        print(f"\n  📡 {msg}")
        assert ok, msg

    def test_browserless_http_health(self):
        """Browserless HTTP health-check."""
        sel_url_str = _get_env("REMOTE_SELENIUM_URL")
        if not sel_url_str:
            pytest.skip("REMOTE_SELENIUM_URL не задан")

        url = urlparse(sel_url_str)
        health_url = f"http://{url.hostname}:{url.port or 3000}/json/version"
        ok, msg = check_http_endpoint(health_url, timeout=10)
        print(f"\n  🌐 {msg}")
        assert ok, msg

    def test_browserless_selenium_connection(self):
        """Selenium Remote WebDriver подключается к Browserless."""
        sel_url_str = _get_env("REMOTE_SELENIUM_URL")
        if not sel_url_str:
            pytest.skip("REMOTE_SELENIUM_URL не задан")

        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Remote(
                command_executor=sel_url_str,
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

    def test_gigachat_api_key_set(self):
        """GIGACHAT_API_KEY задан и не пустой."""
        key = _get_env("GIGACHAT_API_KEY")
        if not key:
            pytest.skip("GIGACHAT_API_KEY не задан")

        assert len(key) > 10, f"GIGACHAT_API_KEY слишком короткий ({len(key)} символов)"
        print(f"\n  🔑 GigaChat API key: {key[:8]}...{key[-4:]}")

    def test_gigachat_client_initialization(self):
        """Клиент GigaChat создаётся без ошибок."""
        key = _get_env("GIGACHAT_API_KEY")
        if not key:
            pytest.skip("GIGACHAT_API_KEY не задан")

        try:
            from gigachat import GigaChat
            giga = GigaChat(
                credentials=key,
                verify_ssl_certs=False,
                model="GigaChat",
            )
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

    def test_kinopoisk_api_key_set(self):
        """KINOPOISK_API_KEY задан."""
        key = _get_env("KINOPOISK_API_KEY")
        if not key:
            pytest.skip("KINOPOISK_API_KEY не задан")

        print(f"\n  🔑 Kinopoisk API key: {key[:8]}...")

    def test_kinopoisk_api_reachable(self):
        """Kinopoisk API доступен."""
        key = _get_env("KINOPOISK_API_KEY")
        if not key:
            pytest.skip("KINOPOISK_API_KEY не задан")

        try:
            from src.out.openapi_client.api_client import ApiClient
            from src.out.openapi_client.api.films_api import FilmsApi
            from src.out.openapi_client.configuration import Configuration

            config = Configuration(api_key={"ApiKeyAuth": key})
            api_client = ApiClient(config)
            api = FilmsApi(api_client)

            response = api.api_v21_films_search_by_keyword_get(keyword="test", page=1)
            assert response is not None
            print(f"\n  🟢 Kinopoisk API — OK")
        except ImportError:
            pytest.skip("openapi_client не установлен")
        except Exception as e:
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
        results = []

        # Redis
        broker_url = _get_env("CELERY_BROKER_URL")
        if broker_url:
            url = urlparse(broker_url)
            ok, msg = check_tcp_connection(url.hostname, url.port or 6379, timeout=3)
            results.append(("Redis", ok, msg))
        else:
            results.append(("Redis", None, "CELERY_BROKER_URL не задан"))

        # PostgreSQL
        db_url = _get_env("DATABASE_URL")
        if db_url:
            clean_url = db_url.replace("postgresql+asyncpg://", "http://").replace("postgresql://", "http://")
            parsed = urlparse(clean_url)
            ok, msg = check_tcp_connection(parsed.hostname, parsed.port or 5432, timeout=3)
            results.append(("PostgreSQL", ok, msg))
        else:
            results.append(("PostgreSQL", None, "DATABASE_URL не задан"))

        # Browserless
        sel_url_str = _get_env("REMOTE_SELENIUM_URL")
        if sel_url_str:
            sel_url = urlparse(sel_url_str)
            ok, msg = check_tcp_connection(sel_url.hostname, sel_url.port or 3000, timeout=3)
            results.append(("Browserless", ok, msg))
        else:
            results.append(("Browserless", None, "REMOTE_SELENIUM_URL не задан"))

        # Telegram
        ok, msg = check_http_endpoint("https://api.telegram.org", timeout=5)
        results.append(("Telegram API", ok, msg))

        # Вывод отчёта
        print("\n" + "=" * 60)
        print("  📊 HEALTH CHECK REPORT")
        print("=" * 60)
        for name, ok, msg in results:
            if ok is None:
                status = "⏭️"
            elif ok:
                status = "✅"
            else:
                status = "❌"
            print(f"  {status} {name}: {msg}")
        print("=" * 60)

        # Проверяем что критические сервисы (если заданы) доступны
        critical = [r for r in results if r[0] in ("Redis", "PostgreSQL") and r[1] is not None]
        failed_critical = [r[0] for r in critical if not r[1]]
        assert not failed_critical, f"Критические сервисы недоступны: {failed_critical}"
