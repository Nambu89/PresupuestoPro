import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de la base de datos
database_url = os.getenv("DATABASE_URL")
print(f"Conectando a: {database_url}")

# Crear el motor de SQLAlchemy
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Importar los modelos
from app.models.user import User
from app.models.project import Project
from app.models.payment import Payment

def initialize_database():
    print("Creando tablas en la base de datos...")
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    print("¡Tablas creadas con éxito!")
    
    # Listar las tablas creadas
    metadata = MetaData()
    metadata.reflect(bind=engine)
    print("\nTablas creadas:")
    for table in metadata.sorted_tables:
        print(f"- {table.name}")

if __name__ == "__main__":
    initialize_database()
