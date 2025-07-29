# app/api/endpoints/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api import deps
from app.models.deadline.model import Deadline, DeadlineClassification
from app.schemas.deadline import DeadlineStatus

router = APIRouter()

@router.get("/")
def get_dashboard_data(db: Session = Depends(deps.get_db)):
    """
    Retorna os dados agregados para a tela de dashboard.
    """
    # Contagem de Prazos Críticos e Fatais
    critical_count = db.query(Deadline).filter(
        Deadline.classification == DeadlineClassification.CRITICO,
        Deadline.status == DeadlineStatus.PENDENTE
    ).count()
    
    fatal_count = db.query(Deadline).filter(
        Deadline.classification == DeadlineClassification.FATAL,
        Deadline.status == DeadlineStatus.PENDENTE
    ).count()

    # Contagem para o gráfico de pizza
    pie_chart_data = db.query(
        Deadline.status, func.count(Deadline.status)
    ).group_by(Deadline.status).all()
    
    # Formata a saída para o frontend
    formatted_pie_data = [{"status": status, "count": count} for status, count in pie_chart_data]
    
    return {
        "critical_count": critical_count,
        "fatal_count": fatal_count,
        "pie_chart_data": formatted_pie_data,
    }