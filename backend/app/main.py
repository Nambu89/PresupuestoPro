from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import auth, user, projects, payments, chat, user_config
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, 
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuración CORS
origins = [
    "http://localhost",
    "http://localhost:5173",  # Frontend Vite default
    "http://localhost:3000",
    "http://localhost:8080",  # Puerto actual del frontend
    "http://localhost:8081",  # Puerto alternativo
    "http://127.0.0.1:8080",  # También permitir acceso por IP
    "http://127.0.0.1:8081",  # También permitir acceso por IP alternativo
    "https://presupuestopro.com",
    # Agregar aquí los orígenes permitidos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],  # Necesario para descargas
)

# Manejo de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred."},
    )

# Endpoints API v1
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(user.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
app.include_router(payments.router, prefix=f"{settings.API_V1_STR}/payments", tags=["payments"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(user_config.router, prefix=f"{settings.API_V1_STR}/config", tags=["config"])

@app.get("/")
def root():
    return {"message": "Bienvenido a PresupuestoPro API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.VERSION}