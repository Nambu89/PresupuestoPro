from typing import Optional
from sqlalchemy.orm import Session

from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentCreate

def create_payment(
    db: Session, 
    payment: PaymentCreate, 
    user_id: int, 
    stripe_payment_id: Optional[str] = None
) -> Payment:
    db_payment = Payment(
        amount=payment.amount,
        currency=payment.currency,
        status=PaymentStatus.PENDING,
        user_id=user_id,
        project_id=payment.project_id,
        stripe_payment_id=stripe_payment_id
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: int) -> Optional[Payment]:
    return db.query(Payment).filter(Payment.id == payment_id).first()

def update_payment_status(
    db: Session, 
    payment_id: int, 
    status: PaymentStatus
) -> Optional[Payment]:
    db_payment = get_payment(db, payment_id)
    if not db_payment:
        return None
    
    db_payment.status = status
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment_by_stripe_id(db: Session, stripe_payment_id: str) -> Optional[Payment]:
    return db.query(Payment).filter(Payment.stripe_payment_id == stripe_payment_id).first()