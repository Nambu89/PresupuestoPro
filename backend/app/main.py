from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app
import time

from app.api import auth, user, projects, payments, chat, user_config
from app.config import settings

# Definir métricas personalizadas
REQUEST_COUNT = Counter(
    'presupuestopro_http_request_count', 
    'Contador de peticiones HTTP', 
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'presupuestopro_http_request_latency_seconds', 
    'Latencia de peticiones HTTP', 
    ['method', 'endpoint']
)

ACTIVE_USERS = Gauge(
    'presupuestopro_active_users_count',
    'Número de usuarios activos'
)

# Nota: Las métricas específicas de la API de IA están definidas en ai.py
# y tienen nombres diferentes para evitar conflictos

app = FastAPI(
    title=settings.PROJECT_NAME, 
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Inicializar Instrumentator para Prometheus
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

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
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/projects", tags=["chat"])
app.include_router(user_config.router, prefix=f"{settings.API_V1_STR}/config", tags=["config"])

# Middleware para métricas personalizadas
@app.middleware("http")
async def add_metrics(request: Request, call_next):
    # No procesar las peticiones a /metrics para evitar bucles
    if request.url.path == "/metrics":
        return await call_next(request)
        
    # Incrementar contador de usuarios activos
    ACTIVE_USERS.inc()
    
    # Registrar tiempo de inicio
    start_time = time.time()
    
    # Procesar la petición
    response = await call_next(request)
    
    # Calcular duración
    duration = time.time() - start_time
    
    # Registrar métricas
    REQUEST_COUNT.labels(
        method=request.method, 
        endpoint=request.url.path,
        status_code=response.status_code
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method, 
        endpoint=request.url.path
    ).observe(duration)
    
    # Decrementar contador de usuarios activos
    ACTIVE_USERS.dec()
    
    return response


@app.get("/")
def root():
    return {"message": "Bienvenido a PresupuestoPro API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.VERSION}