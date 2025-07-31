# app/services/dashboard_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.deadline.model import Deadline
from app.schemas.deadline import DeadlineClassification, DeadlineStatus
from datetime import datetime, timedelta, timezone

def get_dashboard_stats(db: Session) -> dict:
    now = datetime.now(timezone.utc)
    
    criticos = db.query(Deadline).filter(
        Deadline.classification == DeadlineClassification.CRITICO,
        Deadline.status == DeadlineStatus.PENDENTE
    ).count()

    fatais = db.query(Deadline).filter(
        Deadline.classification == DeadlineClassification.FATAL,
        Deadline.status == DeadlineStatus.PENDENTE
    ).count()
    
    # "Próximos do Vencimento" - consideramos prazos pendentes nos próximos 15 dias, por exemplo.
    next_15_days = now + timedelta(days=15)
    proximos = db.query(Deadline).filter(
        Deadline.due_date <= next_15_days,
        Deadline.status == DeadlineStatus.PENDENTE
    ).count()

    status_results = db.query(Deadline.status, func.count(Deadline.status)).group_by(Deadline.status).all()
    # Converte para um dicionário como: {"pendente": 10, "concluido": 25}
    status_counts = {status.value: count for status, count in status_results}
    
    return {
        "criticos": criticos,
        "fatais": fatais,
        "proximos": proximos,
        "status_counts": status_counts
    }