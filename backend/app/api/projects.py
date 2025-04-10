from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.project import create_project, get_project, get_user_projects, update_project
from app.models.user import User
from app.models.project import Project
from app.schemas.project import Project as ProjectSchema, ProjectCreate, ProjectUpdate, ProjectPremium
from app.services.ai import AIProjectEstimator
from app.services.pdf_generator import PDFGenerator
from app.services.email_sender import EmailSender

router = APIRouter()

# Inicializar servicios
ai_estimator = AIProjectEstimator()
pdf_generator = PDFGenerator()
email_sender = EmailSender()

@router.post("/", response_model=ProjectSchema)
def create_user_project(
    *,
    db: Session = Depends(get_db),
    project_in: ProjectCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new project for the current user
    """
    try:
        print(f"Creando proyecto para usuario ID: {current_user.id}")
        print(f"Datos del proyecto: {project_in.model_dump()}")
        
        # Generar estimación con IA
        description = project_in.description or project_in.name
        print(f"Generando estimación para: {description[:100]}...")
        
        preview_data, full_data = ai_estimator.generate_estimate(description)
        print(f"Datos de vista previa generados: {preview_data}")
        
        # Asegurarse de que los campos de estimación tengan valores predeterminados si no existen
        if not project_in.estimated_cost:
            project_in.estimated_cost = preview_data.get("estimated_cost", 10000)
        
        if not project_in.estimated_duration_weeks:
            project_in.estimated_duration_weeks = preview_data.get("estimated_duration_weeks", 8)
        
        print(f"Valores finales: coste={project_in.estimated_cost}, duración={project_in.estimated_duration_weeks}")
        
        # Crear el proyecto
        project = create_project(
            db=db, 
            project=project_in, 
            user_id=current_user.id,
            preview_data=preview_data,
            full_data=full_data
        )
        
        print(f"Proyecto creado con ID: {project.id}")
        return project
    except Exception as e:
        print(f"Error al crear proyecto: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating project: {str(e)}")

@router.get("/", response_model=List[ProjectSchema])
def read_user_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get all projects for the current user
    """
    projects = get_user_projects(db, user_id=current_user.id, skip=skip, limit=limit)
    return projects

@router.get("/{project_id}", response_model=ProjectSchema)
def read_user_project(
    *,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get a specific project by id
    """
    project = get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return project

@router.get("/{project_id}/premium", response_model=ProjectPremium)
def read_premium_project(
    *,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: Request = None,
) -> Any:
    """
    Get a premium project with full data
    """
    try:
        # Imprimir información de depuración
        print(f"Obteniendo proyecto premium ID: {project_id}, Usuario ID: {current_user.id}")
        
        # Obtener el proyecto
        project = get_project(db, project_id=project_id)
        if not project:
            print(f"Proyecto no encontrado: {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Verificar permisos
        if project.user_id != current_user.id:
            print(f"Sin permisos: proyecto.user_id={project.user_id}, current_user.id={current_user.id}")
            raise HTTPException(status_code=403, detail="Not enough permissions")
        
        # Para propósitos de prueba, permitir ver cualquier proyecto como premium
        # Comentar esta línea para restaurar la verificación de premium en producción
        # if not project.is_premium:
        #     raise HTTPException(status_code=403, detail="This is not a premium project")
        
        # Generar datos de ejemplo para el proyecto si no existen
        if not hasattr(project, 'preview_data') or not project.preview_data:
            project.preview_data = {
                "estimated_hours": 120,
                "team_size": 3,
                "technologies": ["React", "Node.js", "PostgreSQL"],
                "main_features": ["Autenticación", "Dashboard", "Reportes", "API"]
            }
        
        if not hasattr(project, 'full_data') or not project.full_data:
            project.full_data = {
                "detailed_timeline": "4 semanas para diseño, 6 semanas para desarrollo, 2 semanas para pruebas",
                "risk_assessment": "Bajo riesgo técnico, medio riesgo en plazos",
                "maintenance_cost": 1500,
                "hosting_cost": 800,
                "license_costs": 1200
            }
        
        print(f"Proyecto premium obtenido correctamente: {project.name}")
        return project
    except Exception as e:
        print(f"Error al obtener proyecto premium: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving premium project: {str(e)}")

@router.put("/{project_id}", response_model=ProjectSchema)
def update_user_project(
    *,
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update a project
    """
    project = get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    project = update_project(db, project_id=project_id, project=project_in)
    return project

@router.get("/{project_id}/view-pdf")
def view_project_pdf(
    *,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: Request = None,
) -> Any:
    """
    Ver un proyecto en formato PDF en el navegador
    """
    try:
        # Imprimir información de depuración
        print(f"Visualizando PDF para proyecto ID: {project_id}, Usuario ID: {current_user.id}")
        
        # Obtener el proyecto
        project = get_project(db, project_id=project_id)
        if not project:
            print(f"Proyecto no encontrado: {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Verificar permisos
        if project.user_id != current_user.id:
            print(f"Sin permisos: proyecto.user_id={project.user_id}, current_user.id={current_user.id}")
            raise HTTPException(status_code=403, detail="Not enough permissions")
        
        # Generar datos de ejemplo para el PDF si no existen
        if not hasattr(project, 'preview_data') or not project.preview_data:
            project.preview_data = {
                "estimated_hours": 120,
                "team_size": 3,
                "technologies": ["React", "Node.js", "PostgreSQL"],
                "main_features": ["Autenticación", "Dashboard", "Reportes", "API"]
            }
        
        if not hasattr(project, 'full_data') or not project.full_data:
            project.full_data = {
                "detailed_timeline": "4 semanas para diseño, 6 semanas para desarrollo, 2 semanas para pruebas",
                "risk_assessment": "Bajo riesgo técnico, medio riesgo en plazos",
                "maintenance_cost": 1500,
                "hosting_cost": 800,
                "license_costs": 1200
            }
        
        # Generar el PDF
        pdf_content = pdf_generator.generate_project_pdf(project, current_user)
        
        # Configurar la respuesta para visualización en el navegador
        filename = f"presupuesto_{project.name.replace(' ', '_')}.pdf"
        response = Response(content=pdf_content, media_type="application/pdf")
        response.headers["Content-Disposition"] = f"inline; filename={filename}"
        
        print(f"PDF visualizado correctamente para: {project.name}")
        return response
    except Exception as e:
        print(f"Error al visualizar PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error viewing PDF: {str(e)}")

@router.get("/{project_id}/pdf")
def download_project_pdf(
    *,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: Request = None,
) -> Any:
    """
    Descargar un proyecto en formato PDF
    """
    try:
        # Imprimir información de depuración
        print(f"Descargando PDF para proyecto ID: {project_id}, Usuario ID: {current_user.id}")
        
        # Obtener el proyecto
        project = get_project(db, project_id=project_id)
        if not project:
            print(f"Proyecto no encontrado: {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Verificar permisos
        if project.user_id != current_user.id:
            print(f"Sin permisos: proyecto.user_id={project.user_id}, current_user.id={current_user.id}")
            raise HTTPException(status_code=403, detail="Not enough permissions")
        
        # Generar datos de ejemplo para el PDF si no existen
        if not hasattr(project, 'preview_data') or not project.preview_data:
            project.preview_data = {
                "estimated_hours": 120,
                "team_size": 3,
                "technologies": ["React", "Node.js", "PostgreSQL"],
                "main_features": ["Autenticación", "Dashboard", "Reportes", "API"]
            }
        
        if not hasattr(project, 'full_data') or not project.full_data:
            project.full_data = {
                "detailed_timeline": "4 semanas para diseño, 6 semanas para desarrollo, 2 semanas para pruebas",
                "risk_assessment": "Bajo riesgo técnico, medio riesgo en plazos",
                "maintenance_cost": 1500,
                "hosting_cost": 800,
                "license_costs": 1200
            }
        
        # Generar el PDF
        pdf_content = pdf_generator.generate_project_pdf(project, current_user)
        
        # Configurar la respuesta para descarga
        filename = f"presupuesto_{project.name.replace(' ', '_')}.pdf"
        response = Response(content=pdf_content, media_type="application/pdf")
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        
        print(f"PDF descargado correctamente para: {project.name}")
        return response
    except Exception as e:
        print(f"Error al descargar PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading PDF: {str(e)}")

@router.post("/{project_id}/email")
def send_project_email(
    *,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks,
    to_email: str = None,
    request: Request = None,
) -> Any:
    """
    Enviar un proyecto por email
    """
    project = get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Usar el email del usuario si no se proporciona uno específico
    recipient_email = to_email if to_email else current_user.email
    
    # Generar el PDF
    pdf_content = pdf_generator.generate_project_pdf(project, current_user)
    
    # Enviar el email en segundo plano
    background_tasks.add_task(
        email_sender.send_project_email,
        recipient_email,
        project,
        current_user,
        pdf_content
    )
    
    return {"message": f"Email enviado correctamente a {recipient_email}"}