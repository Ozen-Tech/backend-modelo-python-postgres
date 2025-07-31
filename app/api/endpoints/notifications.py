# app/api/endpoints/notifications.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user.model import User
from app.schemas.notification import NotificationPublic
from app.services import notification_service

router = APIRouter()

@router.get("/", response_model=list[NotificationPublic])
def list_notifications(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return notification_service.get_notifications_by_user(db=db, user_id=current_user.id)

@router.post("/read-all", status_code=status.HTTP_204_NO_CONTENT)
def mark_all_as_read(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    notification_service.mark_all_as_read(db=db, user_id=current_user.id)
    return None