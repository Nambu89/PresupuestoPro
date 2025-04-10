from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

# Esquemas compartidos
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    estimated_cost: Optional[float] = None
    estimated_duration_weeks: Optional[int] = None

# Esquema para creación de proyecto
class ProjectCreate(ProjectBase):
    pass

# Esquema para actualización de proyecto
class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    is_premium: Optional[bool] = None

# Esquema para datos internos
class ProjectInDB(ProjectBase):
    id: int
    user_id: int
    is_premium: bool
    preview_data: Optional[Dict[str, Any]] = None
    full_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquema para respuestas (limitado por tipo de usuario)
class Project(ProjectBase):
    id: int
    is_premium: bool
    preview_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquema para respuestas premium
class ProjectPremium(Project):
    full_data: Optional[Dict[str, Any]] = None