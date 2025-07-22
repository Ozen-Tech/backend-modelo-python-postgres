from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, users, deadlines
from app.db.base import Base # Importante para o Alembic
from app.db.connection import engine
from app.models.user.model import User # Importante para o Alembic

# Isso cria as tabelas, mas Alembic é o preferido. Deixe comentado ou remova
# se estiver usando Alembic religiosamente.
# Base.metadata.create_all(bind=engine) 

app = FastAPI(
    title="API Bacelar Advocacia - Gestão de Prazos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Mude para origens específicas em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(users.router, prefix="/users", tags=["Usuários"])
api_router.include_router(deadlines.router, prefix="/deadlines", tags=["Prazos"])
app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "ok"}