from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Esta es la configuración de Alembic, edita según sea necesario.
# Para más información sobre esta configuración, consulta:
# https://alembic.sqlalchemy.org/en/latest/tutorial.html

# Interpretar el archivo de configuración para la configuración de Python
# de registro
config = context.config

# Analizando el archivo de configuración especificado en el argumento de línea
# de comandos, o el archivo 'alembic.ini'
fileConfig(config.config_file_name)

# Agregar el modelo MetaData aquí
# para que 'autogenerate' pueda comparar las bases de datos y encontrar diferencias
# import your_app_models
# target_metadata = your_app_models.Base.metadata
import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from app.database import Base
from app.models.user import User
from app.models.project import Project
from app.models.payment import Payment

target_metadata = Base.metadata

# otras configuraciones de valores toman la configuración alembic.ini
# literalmente (no las preprocesa).
# Si quieres usar otra configuración, debes ponerla en una
# variable, como:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
    """Ejecuta migraciones en modo 'offline'.

    Esto configura el contexto con solo una URL
    y no un Engine, aunque un Engine es aceptable
    aquí también. Al omitir el Engine, obtenemos
    las declaraciones de migraciones que se pueden prueben
    ejecutando el script contra una base de datos existente.

    Llamar a connection.execute() aquí generaría el script.

    """
    from app.config import settings
    
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Ejecuta migraciones en modo 'online'.

    En este escenario tenemos acceso al Engine
    y podemos ejecutar migraciones directamente.

    """
    from app.config import settings
    
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()