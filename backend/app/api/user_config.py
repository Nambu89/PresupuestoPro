from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.user_config import get_user_config, create_user_config, update_user_config
from app.models.user import User
from app.schemas.user_config import UserConfig as UserConfigSchema, UserConfigCreate, UserConfigUpdate

router = APIRouter()

@router.get("/", response_model=UserConfigSchema)
def read_user_config(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Obtener la configuración del usuario actual
    """
    config = get_user_config(db, user_id=current_user.id)
    if not config:
        # Si no existe, crear una configuración por defecto
        config = create_user_config(db, user_id=current_user.id, config=UserConfigCreate())
    return config

@router.put("/", response_model=UserConfigSchema)
def update_config(
    *,
    config_in: UserConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Actualizar la configuración del usuario actual
    """
    config = update_user_config(db, user_id=current_user.id, config_in=config_in)
    return config
