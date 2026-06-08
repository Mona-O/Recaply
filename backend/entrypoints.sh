#!/bin/bash
set -e

echo "🚀 Démarrage de Recaply Backend..."

# ============================================================
# 1. Init Alembic si pas encore fait
# ============================================================
if [ ! -d "alembic" ]; then
    echo "⚙️  Initialisation d'Alembic..."
    alembic init alembic

    # Réécrire env.py pour async + import des modèles
    python3 - << 'PYEOF'
content = '''import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from config.database import Base

# -- Ajoute ici tes modèles pour qu Alembic les detecte --
from models.report import Report
# from models.user import User

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''
with open("alembic/env.py", "w") as f:
    f.write(content)
print("✅ alembic/env.py configuré")
PYEOF

fi

# ============================================================
# 2. Réécrire alembic.ini proprement via Python (pas de heredoc)
# ============================================================
python3 - << 'PYEOF'
content = "[alembic]\nscript_location = alembic\nprepend_sys_path = .\nsqlalchemy.url = postgresql://recaply:recaply@postgres:5432/recaply\n\n[loggers]\nkeys = root,sqlalchemy,alembic\n\n[handlers]\nkeys = console\n\n[formatters]\nkeys = generic\n\n[logger_root]\nlevel = WARN\nhandlers = console\nqualname =\n\n[logger_sqlalchemy]\nlevel = WARN\nhandlers =\nqualname = sqlalchemy.engine\n\n[logger_alembic]\nlevel = INFO\nhandlers =\nqualname = alembic\n\n[handler_console]\nclass = StreamHandler\nargs = (sys.stderr,)\nlevel = NOTSET\nformatter = generic\n\n[formatter_generic]\nformat = %%(levelname)-5.5s [%%(name)s] %%(message)s\ndatefmt = %%H:%%M:%%S\n"
with open("alembic.ini", "w") as f:
    f.write(content)
print("✅ alembic.ini ecrit proprement")
PYEOF

# ============================================================
# 3. Attendre que Postgres soit prêt
# ============================================================
echo "⏳ Attente de PostgreSQL..."
until python3 -c "
import asyncio, asyncpg
async def check():
    conn = await asyncpg.connect('postgresql://recaply:recaply@postgres:5432/recaply')
    await conn.close()
asyncio.run(check())
" 2>/dev/null; do
    echo "   PostgreSQL pas encore pret, retry dans 2s..."
    sleep 2
done
echo "✅ PostgreSQL pret"

# ============================================================
# 4. Créer la migration initiale si aucune n'existe
# ============================================================
if [ -z "$(ls -A alembic/versions/ 2>/dev/null)" ]; then
    echo "⚙️  Creation de la migration initiale..."
    alembic revision --autogenerate -m "init"
    echo "✅ Migration initiale creee"
fi

# ============================================================
# 5. Appliquer les migrations
# ============================================================
echo "⏳ Application des migrations..."
alembic upgrade head
echo "✅ Migrations appliquees"

# ============================================================
# 6. Lancer le serveur
# ============================================================
echo "Lancement du serveur..."
exec uvicorn app:app --host 0.0.0.0 --port 8000