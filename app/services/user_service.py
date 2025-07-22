from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user.model import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

def get_user_by_email_or_cpf(db: Session, identifier: str) -> User | None:
    return db.query(User).filter(or_(User.email == identifier, User.cpf == identifier)).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, *, user_in: UserCreate) -> User:
    db_user = User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        name=user_in.name,
        profile=user_in.profile
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, *, identifier: str, password: str) -> User | None:
    user = get_user_by_email_or_cpf(db, identifier=identifier)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user