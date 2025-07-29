# app/api/endpoints/users.py
from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session
from app.schemas.user import UserPublic
from app.schemas.token import FCMTokenPayload
from app.api import deps
from app.models.user.model import User

router = APIRouter()

@router.get("/me", response_model=UserPublic)

@router.post("/me/fcm-token", status_code=status.HTTP_204_NO_CONTENT)
def update_fcm_token(
    payload: FCMTokenPayload = Body(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Recebe e salva o FCM token do aparelho do usuário logado.
    O app mobile deve chamar esta rota após o login e a cada vez que o token mudar.
    """
    current_user.fcm_token = payload.fcm_token
    db.commit()
    return None