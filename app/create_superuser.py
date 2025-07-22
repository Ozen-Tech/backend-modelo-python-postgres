from sqlalchemy.orm import Session
from app.core.config import settings
from app.services import user_service
from app.schemas.user import UserCreate, UserProfile
from app.db.connection import SessionLocal

def init_db(db: Session) -> None:
    # Verifique se já existe um superusuário
    user = user_service.get_user_by_email(db, email=settings.SUPERUSER_EMAIL)
    if not user:
        # Crie o superusuário
        user_in = UserCreate(
            email=settings.SUPERUSER_EMAIL,
            password=settings.SUPERUSER_PASSWORD,
            name="Admin Bacelar",
            profile=UserProfile.ADMIN
        )
        user_service.create_user(db=db, user_in=user_in)
        print(f"Superusuário {settings.SUPERUSER_EMAIL} criado com sucesso.")
    else:
        print(f"Superusuário {settings.SUPERUSER_EMAIL} já existe. Pulando criação.")

if __name__ == "__main__":
    print("Iniciando criação de dados iniciais (superuser)...")
    db = SessionLocal()
    init_db(db)
    db.close()
    print("Criação de dados iniciais concluída.")