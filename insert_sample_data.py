import logging
import sys
import os
import json
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Añadir el directorio actual al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from sqlalchemy import text

def insert_sample_data():
    """
    Inserta datos de ejemplo directamente en la base de datos usando SQL
    """
    db = SessionLocal()
    try:
        # Verificar si ya existe el usuario administrador
        admin_user = db.execute(text("SELECT id FROM users WHERE email = 'fernando.prada@presupuestopro.com'")).first()
        if not admin_user:
            logger.info("No se encontró el usuario administrador. Por favor, asegúrate de que el usuario existe.")
            return
        else:
            admin_id = admin_user[0]
            logger.info(f"Usuario administrador encontrado con ID: {admin_id}")
            
        # Verificar si ya existen proyectos
        projects_count = db.execute(text("SELECT COUNT(*) FROM projects")).scalar()
        if projects_count > 0:
            logger.info(f"Ya existen {projects_count} proyectos en la base de datos")
            return
            
        # Datos de ejemplo para proyectos
        example_projects = [
            {
                "name": "App de Gestión",
                "description": "TechSolutions S.L.\nAplicación de gestión empresarial con módulos de contabilidad, inventario y recursos humanos.",
                "estimated_cost": 12500.0,
                "estimated_duration_weeks": 12,
                "is_premium": True,
                "preview_data": {
                    "estimated_hours": 480,
                    "team_size": 4,
                    "technologies": ["React", "Node.js", "PostgreSQL"],
                    "main_features": ["Autenticación", "Dashboard", "Reportes", "API"]
                },
                "full_data": {
                    "detailed_timeline": "4 semanas para diseño, 6 semanas para desarrollo, 2 semanas para pruebas",
                    "risk_assessment": "Bajo riesgo técnico, medio riesgo en plazos",
                    "maintenance_cost": 1500,
                    "hosting_cost": 800,
                    "license_costs": 1200
                }
            },
            {
                "name": "Tienda Online",
                "description": "Moda Express\nPlataforma de comercio electrónico con catálogo de productos, carrito de compra y pasarela de pago.",
                "estimated_cost": 8900.0,
                "estimated_duration_weeks": 8,
                "is_premium": False,
                "preview_data": {
                    "estimated_hours": 320,
                    "team_size": 3,
                    "technologies": ["Vue.js", "Express", "MongoDB"],
                    "main_features": ["Catálogo", "Carrito", "Pagos", "Usuarios"]
                },
                "full_data": {
                    "detailed_timeline": "3 semanas para diseño, 4 semanas para desarrollo, 1 semana para pruebas",
                    "risk_assessment": "Bajo riesgo técnico, bajo riesgo en plazos",
                    "maintenance_cost": 900,
                    "hosting_cost": 600,
                    "license_costs": 500
                }
            },
            {
                "name": "Dashboard Analytics",
                "description": "DataViz Inc.\nPanel de control con visualización de datos y métricas de rendimiento para toma de decisiones.",
                "estimated_cost": 15200.0,
                "estimated_duration_weeks": 10,
                "is_premium": False,
                "preview_data": {
                    "estimated_hours": 400,
                    "team_size": 3,
                    "technologies": ["D3.js", "Python", "Flask", "PostgreSQL"],
                    "main_features": ["Gráficos interactivos", "Exportación de datos", "Alertas", "Informes"]
                },
                "full_data": {
                    "detailed_timeline": "2 semanas para diseño, 6 semanas para desarrollo, 2 semanas para pruebas",
                    "risk_assessment": "Medio riesgo técnico, bajo riesgo en plazos",
                    "maintenance_cost": 1200,
                    "hosting_cost": 700,
                    "license_costs": 900
                }
            },
            {
                "name": "Aplicación Móvil",
                "description": "Startup Mobile\nApp móvil para Android e iOS con funcionalidades de geolocalización y notificaciones push.",
                "estimated_cost": 18750.0,
                "estimated_duration_weeks": 14,
                "is_premium": False,
                "preview_data": {
                    "estimated_hours": 560,
                    "team_size": 4,
                    "technologies": ["React Native", "Firebase", "Google Maps API"],
                    "main_features": ["Geolocalización", "Notificaciones", "Perfiles", "Chat"]
                },
                "full_data": {
                    "detailed_timeline": "3 semanas para diseño, 8 semanas para desarrollo, 3 semanas para pruebas",
                    "risk_assessment": "Alto riesgo técnico, medio riesgo en plazos",
                    "maintenance_cost": 1800,
                    "hosting_cost": 1200,
                    "license_costs": 1500
                }
            },
            {
                "name": "Rediseño Web Corporativa",
                "description": "Corporación Global\nRediseño completo de sitio web corporativo con enfoque en experiencia de usuario y optimización SEO.",
                "estimated_cost": 7300.0,
                "estimated_duration_weeks": 6,
                "is_premium": True,
                "preview_data": {
                    "estimated_hours": 240,
                    "team_size": 2,
                    "technologies": ["HTML5", "CSS3", "JavaScript", "WordPress"],
                    "main_features": ["Diseño responsive", "Blog", "Formularios", "SEO"]
                },
                "full_data": {
                    "detailed_timeline": "2 semanas para diseño, 3 semanas para desarrollo, 1 semana para pruebas",
                    "risk_assessment": "Bajo riesgo técnico, bajo riesgo en plazos",
                    "maintenance_cost": 600,
                    "hosting_cost": 400,
                    "license_costs": 300
                }
            }
        ]
        
        # Insertar proyectos de ejemplo usando SQL directo
        for project_data in example_projects:
            # Convertir los diccionarios a JSON para almacenarlos
            preview_data_json = json.dumps(project_data["preview_data"])
            full_data_json = json.dumps(project_data["full_data"])
            
            # Crear la consulta SQL para insertar el proyecto
            sql = text("""
                INSERT INTO projects (name, description, estimated_cost, estimated_duration_weeks, 
                                     is_premium, preview_data, full_data, user_id, created_at)
                VALUES (:name, :description, :estimated_cost, :estimated_duration_weeks, 
                       :is_premium, :preview_data, :full_data, :user_id, :created_at)
            """)
            
            # Ejecutar la consulta con los parámetros
            db.execute(sql, {
                "name": project_data["name"],
                "description": project_data["description"],
                "estimated_cost": project_data["estimated_cost"],
                "estimated_duration_weeks": project_data["estimated_duration_weeks"],
                "is_premium": project_data["is_premium"],
                "preview_data": preview_data_json,
                "full_data": full_data_json,
                "user_id": admin_id,
                "created_at": datetime.now()
            })
            
            logger.info(f"Proyecto añadido: {project_data['name']}")
            
        db.commit()
        logger.info("Datos de ejemplo insertados correctamente")
        
    except Exception as e:
        logger.error(f"Error al insertar datos de ejemplo: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Iniciando inserción de datos de ejemplo...")
    insert_sample_data()
    logger.info("Proceso completado.")
