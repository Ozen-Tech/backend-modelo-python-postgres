from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user.model import User
from app.models.notification.model import Notification
from app.schemas.notification import NotificationPublic

router = APIRouter()

@router.get("/", response_model=List[NotificationPublic])
def list_notifications(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Lista todas as notificações do usuário logado, das mais recentes para as mais antigas.
    """
    return db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).limit(100).all()

@router.post("/read-all", status_code=status.HTTP_204_NO_CONTENT)
def mark_all_as_read(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Marca todas as notificações não lidas do usuário como lidas.
    """
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({'is_read': True})
    db.commit()
    return None