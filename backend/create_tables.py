from app.database import Base, engine
from app.models.user import User
from app.models.project import Project
from app.models.payment import Payment

def create_tables():
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas con éxito!")

if __name__ == "__main__":
    create_tables()
