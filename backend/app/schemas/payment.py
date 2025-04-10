from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.payment import PaymentStatus

# Esquemas compartidos
class PaymentBase(BaseModel):
    amount: float
    currency: str = "EUR"

# Esquema para creación de pago
class PaymentCreate(PaymentBase):
    project_id: int

# Esquema para respuestas
class Payment(PaymentBase):
    id: int
    status: PaymentStatus
    project_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquema para respuesta de pago con Stripe
class PaymentResponse(BaseModel):
    payment_id: int
    checkout_url: str