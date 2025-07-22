from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.token import Token
from app.services import user_service
from app.core.security import create_access_token
from app.api import deps

router = APIRouter()

@router.post("/login", response_model=Token)
def login_for_access_token(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_service.authenticate_user(db, identifier=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email/CPF ou senha incorretos")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
        
    access_token = create_access_token(data={"sub": user.email, "profile": user.profile.value})
    return {"access_token": access_token, "token_type": "bearer"}