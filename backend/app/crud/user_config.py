from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.models.user_config import UserConfig
from app.schemas.user_config import UserConfigCreate, UserConfigUpdate


def get_user_config(db: Session, user_id: int) -> Optional[UserConfig]:
    """
    Obtiene la configuración de un usuario por su ID
    """
    return db.query(UserConfig).filter(UserConfig.user_id == user_id).first()


def create_user_config(db: Session, *, user_id: int, config: UserConfigCreate) -> UserConfig:
    """
    Crea una nueva configuración para un usuario
    """
    db_config = UserConfig(
        user_id=user_id,
        notification_email=config.notification_email,
        notification_sms=config.notification_sms,
        language=config.language,
        theme=config.theme,
        currency=config.currency
    )
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


def update_user_config(
    db: Session, *, user_id: int, config_in: Union[UserConfigUpdate, Dict[str, Any]]
) -> UserConfig:
    """
    Actualiza la configuración de un usuario
    """
    db_config = get_user_config(db, user_id=user_id)
    if not db_config:
        # Si no existe, crear una nueva configuración
        if isinstance(config_in, dict):
            config_data = config_in
        else:
            config_data = config_in.dict(exclude_unset=True)
        return create_user_config(db, user_id=user_id, config=UserConfigCreate(**config_data))
    
    # Actualizar configuración existente
    if isinstance(config_in, dict):
        update_data = config_in
    else:
        update_data = config_in.dict(exclude_unset=True)
    
    for field in update_data:
        if update_data[field] is not None:
            setattr(db_config, field, update_data[field])
    
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


def delete_user_config(db: Session, *, user_id: int) -> bool:
    """
    Elimina la configuración de un usuario
    """
    db_config = get_user_config(db, user_id=user_id)
    if not db_config:
        return False
    
    db.delete(db_config)
    db.commit()
    return True
