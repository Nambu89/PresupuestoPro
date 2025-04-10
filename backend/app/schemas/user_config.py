from typing import Optional
from pydantic import BaseModel, EmailStr

class UserConfigBase(BaseModel):
    notification_email: bool = True
    notification_sms: bool = False
    language: str = "es"
    theme: str = "light"
    currency: str = "EUR"

class UserConfigCreate(UserConfigBase):
    pass

class UserConfigUpdate(UserConfigBase):
    notification_email: Optional[bool] = None
    notification_sms: Optional[bool] = None
    language: Optional[str] = None
    theme: Optional[str] = None
    currency: Optional[str] = None

class UserConfig(UserConfigBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
