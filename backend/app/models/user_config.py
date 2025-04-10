from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class UserConfig(Base):
    __tablename__ = "user_configs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notification_email = Column(Boolean, default=True)
    notification_sms = Column(Boolean, default=False)
    language = Column(String, default="es")
    theme = Column(String, default="light")
    currency = Column(String, default="EUR")
    
    # Relaciones
    user = relationship("User", back_populates="config")
