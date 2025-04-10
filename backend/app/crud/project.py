from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

def get_project(db: Session, project_id: int) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id).first()

def get_user_projects(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
    return db.query(Project).filter(Project.user_id == user_id).offset(skip).limit(limit).all()

def create_project(db: Session, project: ProjectCreate, user_id: int, 
                  preview_data: Optional[Dict[str, Any]] = None,
                  full_data: Optional[Dict[str, Any]] = None) -> Project:
    db_project = Project(
        **project.model_dump(),
        user_id=user_id,
        preview_data=preview_data,
        full_data=full_data,
        is_premium=False
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project: ProjectUpdate) -> Optional[Project]:
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    update_data = project.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

def set_project_premium(db: Session, project_id: int) -> Optional[Project]:
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    db_project.is_premium = True
    db.commit()
    db.refresh(db_project)
    return db_project