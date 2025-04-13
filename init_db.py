import logging
import sys
import os

# Añadir el directorio actual al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app import crud, schemas
from app.config import settings
# Importar todos los modelos para asegurar que se creen todas las tablas
from app.models import User, Project, UserConfig
from app.services.ai import AIProjectEstimator
from app.database import SessionLocal, Base, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Datos de ejemplo para inicializar
EXAMPLE_PROJECTS = [
    {
        "name": "App de Gestión",
        "description": "Aplicación de gestión empresarial con módulos de contabilidad, inventario y recursos humanos.",
        "client": "TechSolutions S.L.",
        "estimated_cost": 12500,
        "estimated_duration_weeks": 12,
        "status": "Completo",
        "is_premium": True
    },
    {
        "name": "Tienda Online",
        "description": "Plataforma de comercio electrónico con catálogo de productos, carrito de compra y pasarela de pago.",
        "client": "Moda Express",
        "estimated_cost": 8900,
        "estimated_duration_weeks": 8,
        "status": "Vista Previa",
        "is_premium": False
    },
    {
        "name": "Dashboard Analytics",
        "description": "Panel de control con visualización de datos y métricas de rendimiento para toma de decisiones.",
        "client": "DataViz Inc.",
        "estimated_cost": 15200,
        "estimated_duration_weeks": 10,
        "status": "Vista Previa",
        "is_premium": False
    },
    {
        "name": "Aplicación Móvil",
        "description": "App móvil para Android e iOS con funcionalidades de geolocalización y notificaciones push.",
        "client": "Startup Mobile",
        "estimated_cost": 18750,
        "estimated_duration_weeks": 14,
        "status": "Borrador",
        "is_premium": False
    },
    {
        "name": "Rediseño Web Corporativa",
        "description": "Rediseño completo de sitio web corporativo con enfoque en experiencia de usuario y optimización SEO.",
        "client": "Corporación Global",
        "estimated_cost": 7300,
        "estimated_duration_weeks": 6,
        "status": "Completo",
        "is_premium": True
    }
]

def create_tables() -> None:
    """
    Crea todas las tablas definidas en los modelos
    """
    logger.info("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas creadas correctamente")

def init_db() -> None:
    """
    Inicializa la base de datos con datos de ejemplo
    """
    # Primero crear todas las tablas
    create_tables()
    
    db = SessionLocal()
    try:
        # Crear usuario administrador si no existe
        user = crud.user.get_user_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
        if not user:
            user_in = schemas.UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                first_name="Fernando",
                last_name="Prada",
                is_superuser=True,
            )
            user = crud.user.create_user(db, user=user_in)
            logger.info(f"Usuario administrador creado: {user.email}")
        else:
            logger.info(f"Usuario administrador ya existe: {user.email}")
        
        # Verificar si ya existen proyectos
        existing_projects = db.query(Project).filter(Project.user_id == user.id).count()
        if existing_projects > 0:
            logger.info(f"Ya existen {existing_projects} proyectos en la base de datos")
            return
        
        # Crear proyectos de ejemplo
        ai_estimator = AIProjectEstimator()
        
        for project_data in EXAMPLE_PROJECTS:
            # Generar datos de IA
            preview_data, full_data = ai_estimator.generate_estimate(project_data["description"])
            
            # Crear objeto ProjectCreate
            project_in = schemas.ProjectCreate(
                name=project_data["name"],
                description=project_data["description"],
                estimated_cost=project_data["estimated_cost"],
                estimated_duration_weeks=project_data["estimated_duration_weeks"]
            )
            
            # Crear proyecto
            project = crud.project.create_project(
                db=db,
                project=project_in,
                user_id=user.id,
                preview_data=preview_data,
                full_data=full_data
            )
            
            # Actualizar estado y premium
            if project_data["is_premium"]:
                crud.project.set_project_premium(db, project_id=project.id)
            
            logger.info(f"Proyecto creado: {project.name}")
        
        logger.info("Base de datos inicializada con datos de ejemplo")
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Inicializando base de datos con datos de ejemplo")
    init_db()
    logger.info("Base de datos inicializada")
