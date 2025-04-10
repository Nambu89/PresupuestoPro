import stripe
from typing import Optional, Dict, Any

from app.config import settings
from app.models.payment import PaymentStatus

# Configurar Stripe
stripe.api_key = settings.STRIPE_API_KEY

class PaymentService:
    @staticmethod
    def create_checkout_session(
        project_id: int,
        payment_id: int,
        amount: float,
        user_email: str,
        success_url: str,
        cancel_url: str
    ) -> Optional[Dict[str, Any]]:
        try:
            # Convertir a centavos para Stripe
            amount_cents = int(amount * 100)
            
            # Crear sesión de checkout
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "eur",
                            "product_data": {
                                "name": f"Informe Premium - Proyecto #{project_id}",
                                "description": "Acceso al informe completo de presupuesto con detalles detallados.",
                            },
                            "unit_amount": amount_cents,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=f"{success_url}?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=cancel_url,
                customer_email=user_email,
                metadata={
                    "payment_id": str(payment_id),
                    "project_id": str(project_id)
                }
            )
            
            return {
                "id": checkout_session.id,
                "url": checkout_session.url,
            }
            
        except Exception as e:
            print(f"Error creating checkout session: {e}")
            return None
    
    @staticmethod
    def verify_webhook_signature(payload: bytes, signature: str) -> bool:
        try:
            # Verificar que el webhook es legítimo de Stripe
            stripe.Webhook.construct_event(
                payload, signature, settings.STRIPE_WEBHOOK_SECRET
            )
            return True
        except Exception as e:
            print(f"Webhook verification error: {e}")
            return False
    
    @staticmethod
    def handle_payment_intent_succeeded(payment_intent: Dict[str, Any]) -> PaymentStatus:
        # Procesar el pago exitoso
        return PaymentStatus.COMPLETED