from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserPublic
from app.api import deps
from app.models.user.model import User

router = APIRouter()

@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: User = Depends(deps.get_current_active_user)):
    """Retorna os dados do usuário atualmente logado."""
    return current_user