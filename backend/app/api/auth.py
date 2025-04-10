from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import create_access_token, settings
from app.crud.user import authenticate_user, create_user
from app.schemas.user import User, UserCreate, UserLogin
from app.schemas.token import Token

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