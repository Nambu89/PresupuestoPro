from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    
    # Estimaciones
    estimated_cost = Column(Float)
    estimated_duration_weeks = Column(Integer)
    
    # Datos del presupuesto
    preview_data = Column(JSON)  # Datos disponibles en versión gratuita
    full_data = Column(JSON)     # Datos completos (premium)
    
    # Estado del proyecto
    is_premium = Column(Boolean, default=False)
    
    # Relaciones
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="projects")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())