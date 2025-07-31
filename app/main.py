# app/main.py
from fastapi import FastAPI, APIRouter, Request # Adicione 'Request'
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, users, deadlines, dashboard, notifications
from app.core.config import settings

# ------------------
# CRIAÇÃO DAS INSTÂNCIAS
# ------------------
app = FastAPI(
    title="API Bacelar Advocacia - Gestão de Prazos",
    version="1.0.0"
)

api_router = APIRouter(prefix="/api/v1")

# ------------------
# MONTAGEM DOS ROUTERS (Ordem Correta)
# Primeiro, adicionamos TODAS as rotas específicas ao api_router.
# ------------------
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(users.router, prefix="/users", tags=["Usuários"])
api_router.include_router(deadlines.router, prefix="/deadlines", tags=["Prazos"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notificações"])

# ------------------
# INCLUSÃO FINAL E MIDDLEWARES
# Por último, incluímos o api_router já completo no app principal.
# ------------------
app.include_router(api_router)

origins = [
    "http://localhost:5173",
    settings.FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------
# ENDPOINTS GLOBAIS E DE DEPURAÇÃO
# ------------------

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "ok"}

# --- O ENDPOINT MÁGICO DE DEPURAÇÃO ---
# Esta rota vai listar todas as rotas que o FastAPI conhece.
@app.get("/routes", tags=["Debug"])
def list_routes(req: Request):
    return [{"path": route.path, "name": route.name, "methods": route.methods} for route in req.app.routes]
# ----------------------------------------