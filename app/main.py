from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, users, deadlines, dashboard, notifications
from app.db.base import Base 
from app.db.connection import engine
from app.models.user.model import User 
from app.core.config import settings

# Isso cria as tabelas, mas Alembic é o preferido. Deixe comentado ou remova
# se estiver usando Alembic religiosamente.
# Base.metadata.create_all(bind=engine) 

app = FastAPI(
    title="API Bacelar Advocacia - Gestão de Prazos",
    version="1.0.0"
)

origins = [
    settings.FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(users.router, prefix="/users", tags=["Usuários"])
api_router.include_router(deadlines.router, prefix="/deadlines", tags=["Prazos"])
app.include_router(api_router)
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notificações"])

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "ok"}