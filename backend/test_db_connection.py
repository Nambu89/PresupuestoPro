import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de la base de datos
database_url = os.getenv("DATABASE_URL")
print(f"Intentando conectar a: {database_url}")

try:
    # Crear el motor de SQLAlchemy
    engine = create_engine(database_url)
    
    # Intentar conectar
    with engine.connect() as connection:
        print("¡Conexión exitosa a la base de datos!")
        
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
