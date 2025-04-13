import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import ClassVar

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "PresupuestoPro API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    VERSION: str = "1.0.0"
    
    # Configuración de la base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/presupuestopro")
    
    # Configuración de JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 días
    
    # Configuración de Stripe (para pagos)
    STRIPE_API_KEY: str = os.getenv("STRIPE_API_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    
    # Precio del informe completo (en centavos)
    PREMIUM_REPORT_PRICE: int = 500  # 5€

    # URL del frontend
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # Configuración de correo electrónico
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAILS_FROM_EMAIL: str = os.getenv("EMAILS_FROM_EMAIL", "info@presupuestopro.com")
    EMAILS_FROM_NAME: str = os.getenv("EMAILS_FROM_NAME", "PresupuestoPro")

    # Configuración del modelo Pydantic (reemplaza la clase Config)
    model_config = {
        "env_file": ".env",
        "extra": "ignore"  # Permite campos adicionales
    }

settings = Settings()