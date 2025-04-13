from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.crud.project import get_project
from app.services.ai_chat import AIChat

router = APIRouter()

# Inicializar servicio de chat IA
ai_chat = AIChat()

class ChatQuery(BaseModel):
    query: str

@router.post("/{project_id}")
def chat_with_ai(
    *,
    project_id: int,
    chat_query: ChatQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Consultar a la IA sobre un proyecto específico
    """
    # Verificar que el proyecto existe y pertenece al usuario
    project = get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Obtener respuesta de la IA
    response = ai_chat.get_response(project, chat_query.query)
    
    return response
