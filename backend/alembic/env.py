import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# This will correctly allow Alembic to work even with multi-environment setups
from app import models, database  # Adjust 'app' and 'database' as per your project structure

# Read database URL from environment variable or configuration file
DB_URL = os.getenv('DATABASE_URL') or "postgresql://user:password@localhost:5432/db"

# Customize for your project's metadata
metadata = models.Base.metadata  # Replace 'models.Base.metadata' with your actual metadata object

# Alembic configuration
config = context.config
config.set_main_option('sqlalchemy.url', DB_URL)

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Ensure tables are created in the database
target_metadata = metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# When Alembic runs in 'offline' mode, ensure to call 'run_migrations_offline()'
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
