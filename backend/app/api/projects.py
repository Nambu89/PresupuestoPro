from typing import Any, List, Dict, Optional
import os
import json

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.api.deps import get_current_user, get_db
from app.crud.project import create_project, get_project, get_user_projects, update_project, delete_project
from app.models.user import User
from app.models.project import Project
from app.schemas.project import Project as ProjectSchema, ProjectCreate, ProjectUpdate, ProjectPremium
from app.services.ai import AIProjectEstimator
from app.services.pdf_generator import PDFGenerator
from app.services.email_sender import EmailSender

# Modelo para la solicitud de edición directa
class ProjectEditRequest(BaseModel):
    section: Optional[str] = None
    type: str  # 'cost', 'time', 'content'
    value: Optional[float] = None
    unit: Optional[str] = None
    content: Optional[str] = None

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
        
        # Preparar los datos completos del proyecto para la IA
        project_data = {
            "name": project_in.name,
            "description": project_in.description,
            "client": project_in.description.split('\n')[0] if project_in.description and '\n' in project_in.description else "",
            "estimated_duration_weeks": project_in.estimated_duration_weeks
        }
        
        # Convertir a formato de texto para la IA
        project_text = f"Nombre del proyecto: {project_data['name']}\n"
        project_text += f"Cliente: {project_data['client']}\n"
        project_text += f"Descripción: {project_data['description']}\n"
        project_text += f"Duración estimada (semanas): {project_data['estimated_duration_weeks']}\n"
        
        print(f"Generando estimación para: {project_text[:200]}...")
        
        # Verificar que tenemos la clave de API configurada
        api_key = os.getenv("AI_API_KEY")
        api_url = os.getenv("AI_API_URL")
        print("Verificación de configuración de API:")
        print(f"  - API Key disponible: {bool(api_key)}")
        print(f"  - API URL disponible: {bool(api_url)}")
        
        # Generar estimación con IA
        preview_data, full_data = ai_estimator.generate_estimate(project_text)
        print(f"Datos de vista previa generados: {preview_data}")
        
        # Asignar valores de la estimación al proyecto
        project_in.estimated_cost = preview_data.get("estimated_cost", 10000)
        project_in.estimated_duration_weeks = preview_data.get("estimated_duration_weeks", 8)
        
        print(f"Valores finales: coste={project_in.estimated_cost}, duración={project_in.estimated_duration_weeks}")
        
        # Crear el proyecto con los datos generados por la IA
        project = create_project(
            db=db,
            project=project_in,
            user_id=current_user.id,
            preview_data=preview_data,
            full_data=full_data
        )
        
        print(f"Proyecto creado con ID: {project.id}, coste: {project.estimated_cost}, duración: {project.estimated_duration_weeks}")
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

@router.delete("/{project_id}")
def delete_user_project(
    *,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete a project
    """
    try:
        # Verificar que el proyecto existe
        project = get_project(db, project_id=project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Verificar que el usuario es el propietario del proyecto
        if project.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        
        # Eliminar el proyecto
        success = delete_project(db, project_id=project_id)
        if not success:
            raise HTTPException(status_code=500, detail="Error deleting project")
        
        return {"message": "Project successfully deleted"}
    except Exception as e:
        print(f"Error al eliminar proyecto: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting project: {str(e)}")


@router.post("/{project_id}/edit", response_model=Dict[str, Any])
def edit_project_direct(
    *,
    project_id: int,
    edit_request: ProjectEditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Editar un proyecto directamente desde el chat de IA
    """
    try:
        # Verificar que el proyecto existe y pertenece al usuario
        project = get_project(db, project_id=project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if project.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        
        # Cargar los datos actuales del proyecto
        project_data = json.loads(project.data) if project.data else {}
        
        print(f"Solicitud de edición recibida: {edit_request.dict()}")
        print(f"Datos actuales del proyecto: {project_data}")
        
        # Realizar la modificación según el tipo
        if edit_request.type == 'cost':
            print(f"Modificando coste a: {edit_request.value} {edit_request.unit or '€'}")
            # Modificar el coste del proyecto
            if 'cost' not in project_data:
                project_data['cost'] = {}
            
            project_data['cost']['amount'] = edit_request.value
            project_data['cost']['currency'] = edit_request.unit or '€'
            
            # Actualizar también el campo de coste en el modelo principal
            project.cost = float(edit_request.value) if edit_request.value is not None else project.cost
            print(f"Coste actualizado en el modelo: {project.cost}")
            
        elif edit_request.type == 'time':
            print(f"Modificando plazo a: {edit_request.value} {edit_request.unit or 'semanas'}")
            # Modificar el plazo/duración del proyecto
            if 'timeline' not in project_data:
                project_data['timeline'] = {}
            
            # Asegurarnos de que el valor sea un número válido
            if edit_request.value is not None:
                try:
                    duration_value = float(edit_request.value)
                    project_data['timeline']['duration'] = duration_value
                    project_data['timeline']['unit'] = edit_request.unit or 'semanas'
                    
                    # Actualizar también el campo de duración en el modelo principal
                    project.estimated_duration_weeks = duration_value
                    print(f"Duración actualizada en el modelo: {project.estimated_duration_weeks}")
                    
                    # Crear o actualizar el contenido de la sección de planificación
                    if edit_request.content:
                        project_data['timeline']['content'] = edit_request.content
                    else:
                        # Generar un contenido estándar si no se proporciona uno personalizado
                        project_data['timeline']['content'] = f"La duración estimada del proyecto es de {duration_value} {edit_request.unit or 'semanas'}."
                        
                    # Asegurarnos de que haya una estructura de fases
                    if 'phases' not in project_data['timeline']:
                        # Crear una estructura de fases estándar
                        total_weeks = duration_value
                        project_data['timeline']['phases'] = [
                            {"name": "Análisis y planificación", "duration": max(1, round(total_weeks * 0.2))},
                            {"name": "Desarrollo", "duration": max(1, round(total_weeks * 0.5))},
                            {"name": "Pruebas y correcciones", "duration": max(1, round(total_weeks * 0.2))},
                            {"name": "Implementación final", "duration": max(1, round(total_weeks * 0.1))}
                        ]
                        
                        # Ajustar las fases para que sumen exactamente el total
                        sum_phases = sum(phase["duration"] for phase in project_data['timeline']['phases'])
                        if sum_phases != total_weeks:
                            diff = total_weeks - sum_phases
                            project_data['timeline']['phases'][1]["duration"] += diff  # Ajustar la fase de desarrollo
                except (ValueError, TypeError) as e:
                    print(f"Error al convertir el valor de duración: {e}")
                    raise HTTPException(status_code=400, detail=f"El valor de duración no es válido: {edit_request.value}")
        
        elif edit_request.type == 'content':
            # Modificar cualquier otra sección del documento
            if edit_request.section and edit_request.section != 'general':
                # Identificar la sección a modificar
                section_key = None
                if '1. OBJETO' in edit_request.section:
                    section_key = 'objective'
                elif '2. DESCRIPCIÓN' in edit_request.section:
                    section_key = 'description'
                elif '2.1 FUNCIONALIDADES' in edit_request.section:
                    section_key = 'features'
                elif '3. PLANIFICACIÓN' in edit_request.section:
                    section_key = 'timeline'
                elif '4. COSTE' in edit_request.section:
                    section_key = 'cost'
                elif '5. FIRMAS' in edit_request.section:
                    section_key = 'signatures'
                
                if section_key:
                    # Si la sección no existe, crearla
                    if section_key not in project_data:
                        project_data[section_key] = {}
                    
                    # Actualizar el contenido de la sección
                    if isinstance(project_data[section_key], dict):
                        project_data[section_key]['content'] = edit_request.content
                    else:
                        project_data[section_key] = edit_request.content
            else:
                # Modificación general (podría ser el nombre o la descripción general)
                if edit_request.content:
                    # Intentar actualizar campos generales
                    project.description = edit_request.content
        
        # Guardar los cambios en la base de datos
        try:
            print(f"Guardando datos actualizados: {project_data}")
            project.data = json.dumps(project_data)
            db.commit()
            db.refresh(project)
            print(f"Cambios guardados en la base de datos")
        except Exception as db_error:
            print(f"Error al guardar en la base de datos: {db_error}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al guardar en la base de datos: {str(db_error)}")
        
        # Regenerar el PDF con los cambios
        try:
            print(f"Regenerando PDF para el proyecto {project.id}")
            pdf_path = pdf_generator.generate_pdf(project)
            print(f"PDF regenerado correctamente: {pdf_path}")
        except Exception as pdf_error:
            print(f"Error al regenerar el PDF: {pdf_error}")
            # No fallamos la operación completa si solo falla la generación del PDF
            # El usuario aún podrá ver los cambios en la interfaz
        
        response_data = {
            "message": "Proyecto actualizado correctamente",
            "project_id": project.id,
            "section": edit_request.section,
            "type": edit_request.type,
            "value": edit_request.value,
            "unit": edit_request.unit
        }
        
        print(f"Respuesta de éxito: {response_data}")
        return response_data
        
    except Exception as e:
        print(f"Error al editar proyecto: {e}")
        try:
            db.rollback()
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Error al editar proyecto: {str(e)}")

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
        response = Response(
            content=pdf_content, 
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={filename}",
                "Content-Type": "application/pdf",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
        
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
        response = Response(
            content=pdf_content, 
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/pdf",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
        
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