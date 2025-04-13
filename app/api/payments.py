from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.project import create_project, get_project, get_user_projects, update_project
from app.models.user import User
from app.models.project import Project
from app.schemas.project import Project as ProjectSchema, ProjectCreate, ProjectUpdate, ProjectPremium
from app.services.ai import AIProjectEstimator

router = APIRouter()

# Inicializar el servicio de IA
ai_estimator = AIProjectEstimator()

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
    # Generar estimación con IA
    preview_data, full_data = ai_estimator.generate_estimate(project_in.description or project_in.name)
    
    # Actualizar los campos de estimación
    project_in.estimated_cost = preview_data.get("estimated_cost")
    project_in.estimated_duration_weeks = preview_data.get("estimated_duration_weeks")
    
    # Crear el proyecto
    project = create_project(
        db=db, 
        project=project_in, 
        user_id=current_user.id,
        preview_data=preview_data,
        full_data=full_data
    )
    return project

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
) -> Any:
    """
    Get a premium project with full data
    """
    project = get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not project.is_premium:
        raise HTTPException(status_code=402, detail="This project is not premium. Please upgrade to access full data.")
    
    return project

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