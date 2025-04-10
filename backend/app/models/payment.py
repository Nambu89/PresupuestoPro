from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="EUR")
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    stripe_payment_id = Column(String)
    
    # Relaciones
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())