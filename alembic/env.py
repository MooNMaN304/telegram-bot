from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from src.settings import settings
from src.base.base_model import Base

# ВАЖНО: импорт моделей, чтобы Alembic их увидел
from src.db.movies.movie_model import MovieModel
from src.db.cinemas.cinema_model import CinemaModel
from src.db.sessions.session_model import SessionModel
from src.db.user.user_model import UserModel
from src.settings import settings


# Alembic Config
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
# логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# метаданные моделей
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Миграции без подключения к БД"""
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Миграции с подключением к БД"""

    # 👇 ВАЖНО: подставляем URL из settings
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
