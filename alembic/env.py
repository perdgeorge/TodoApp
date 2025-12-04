from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from src.core.config import config as app_config
from src.db.base import Base
from src.db.models.users import User  # noqa: F401
from src.db.models.todos import Todo  # noqa: F401


alembic_config = context.config

url_from_cfg = alembic_config.get_main_option("sqlalchemy.url")
if url_from_cfg == "driver://user:pass@localhost/dbname":
    url_from_cfg = app_config.DB_URL
db_url = url_from_cfg
alembic_config.set_main_option("sqlalchemy.url", db_url)

if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
