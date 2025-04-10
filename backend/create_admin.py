from app.models.user import User
from app.core.security import get_password_hash
from app.database import SessionLocal

def create_admin_user():
    # Crear una sesión de base de datos
    db = SessionLocal()
    
    try:
        # Definir datos del administrador
        admin_email = "fernando.prada@presupuestopro.com"
        admin_password = "Admin123456"  # Asegúrate de cambiar esta contraseña después
        
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(User.email == admin_email).first()
        
        if existing_user:
            print(f"\nEl usuario administrador con email {admin_email} ya existe.")
            # Actualizar a superusuario si no lo es
            if not existing_user.is_superuser:
                existing_user.is_superuser = True
                db.commit()
                print("Usuario actualizado a superusuario.")
            return
        
        # Crear nuevo usuario administrador
        admin_user = User(
            email=admin_email,
            first_name="Fernando",
            last_name="Prada",
            hashed_password=get_password_hash(admin_password),
            is_active=True,
            is_superuser=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"\nUsuario administrador creado con éxito:")
        print(f"Email: {admin_user.email}")
        print(f"Nombre: {admin_user.first_name} {admin_user.last_name}")
        print(f"Contraseña: {admin_password}")
        print(f"Superusuario: {admin_user.is_superuser}")
        print("\nGuarda estas credenciales en un lugar seguro.")
    
    except Exception as e:
        print(f"\nError al crear usuario administrador: {e}")
        db.rollback()
    
    finally:
        db.close()

if __name__ == "__main__":
    print("Creando usuario administrador para PresupuestoPro...")
    create_admin_user()
