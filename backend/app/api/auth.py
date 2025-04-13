from datetime import timedelta
from typing import Any
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.core.security import create_access_token, settings, verify_password, get_password_hash
from app.crud.user import authenticate_user, create_user, get_user, update_user
from app.schemas.user import User, UserCreate, UserLogin, UserUpdate
from app.schemas.token import Token
from app.models.user import User as UserModel

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        print(f"Intento de inicio de sesión con username: {form_data.username}")
        user = authenticate_user(db, email=form_data.username, password=form_data.password)
        if not user:
            print(f"Autenticación fallida para {form_data.username}: usuario no encontrado o contraseña incorrecta")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        print(f"Autenticación exitosa para {form_data.username}")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(user.id, expires_delta=access_token_expires)
        print(f"Token generado con éxito")
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    except Exception as e:
        print(f"Error en login_access_token: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise

@router.post("/register", response_model=User)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Register a new user
    """
    user = create_user(db, user_in)
    return user

@router.get("/me", response_model=User)
def get_current_user_profile(
    current_user: UserModel = Depends(get_current_user),
) -> Any:
    """
    Get current user profile
    """
    return current_user

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

@router.post("/change-password")
def change_password(
    *,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
    password_data: PasswordChange,
) -> Any:
    """
    Change user password
    """
    try:
        print(f"Intentando cambiar contraseña para usuario ID: {current_user.id}")
        print(f"Datos recibidos: {password_data}")
        
        # Verificar que la contraseña actual sea correcta
        if not verify_password(password_data.current_password, current_user.hashed_password):
            print(f"Contraseña actual incorrecta para usuario ID: {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password",
            )
        
        # Actualizar la contraseña
        hashed_password = get_password_hash(password_data.new_password)
        user_in = UserUpdate(hashed_password=hashed_password)
        user = update_user(db, db_obj=current_user, obj_in=user_in)
        print(f"Contraseña actualizada correctamente para usuario ID: {current_user.id}")
        
        return {"message": "Password updated successfully"}
    except Exception as e:
        print(f"Error al cambiar contraseña: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error changing password: {str(e)}",
        )