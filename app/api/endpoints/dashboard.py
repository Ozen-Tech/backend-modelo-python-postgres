# app/api/endpoints/dashboard.py (CORRIGIDO)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.services import dashboard_service
from app.schemas.dashboard import DashboardStats
from app.models.user.model import User

router = APIRouter()

@router.get("/stats", response_model=DashboardStats) # <--- A CORREÇÃO É AQUI
def get_dashboard_statistics(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Obtém as estatísticas para o dashboard principal."""
    return dashboard_service.get_dashboard_stats(db=db)