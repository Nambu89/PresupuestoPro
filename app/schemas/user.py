from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Esquemas compartidos
class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True

# Esquema para creación de usuario
class UserCreate(UserBase):
    password: str

# Esquema para actualización de usuario
class UserUpdate(UserBase):
    password: Optional[str] = None

# Esquema para respuestas
class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquema para respuestas públicas (sin datos sensibles)
class User(UserInDB):
    pass

# Esquema para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str