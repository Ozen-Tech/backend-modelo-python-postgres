# app/main.py
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, users, deadlines, dashboard, notifications
from app.core.config import settings

app = FastAPI(title="API Bacelar Advocacia", version="1.0.0")

# --- A CORREÇÃO DE CORS ESTÁ AQUI ---
# Usamos um regex que aceita tanto http quanto https
# e permite subdomínios (importante para os deploys da Vercel)
ALLOWED_ORIGIN_REGEX = r"https?:\/\/.*\.vercel\.app"

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Para desenvolvimento
    allow_origin_regex=ALLOWED_ORIGIN_REGEX, # Para produção na Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------------------

api_router = APIRouter(prefix="/api/v1")
# (O resto do código dos routers continua o mesmo)
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(users.router, prefix="/users", tags=["Usuários"])
api_router.include_router(deadlines.router, prefix="/deadlines", tags=["Prazos"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notificações"])

app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "ok"}