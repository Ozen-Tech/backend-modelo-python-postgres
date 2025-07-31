# manage.py
import typer
import getpass
from sqlalchemy.orm import Session
from app.db.connection import SessionLocal
from app.services import user_service
from app.schemas.user import UserCreate, UserProfile

# Importa todos os modelos para "aquecer" o SQLAlchemy
from app.db import base

cli_app = typer.Typer()

@cli_app.command()
def create_user():
    """
    Cria um novo usuário no sistema de forma interativa.
    """
    print("--- 🚀 Criando Novo Usuário (Conectado ao Banco) ---")
    
    db: Session = SessionLocal()
    
    try:
        nome = typer.prompt("Nome completo")
        email = typer.prompt("E-mail")
        
        # Validação
        if user_service.get_user_by_email(db, email=email):
            print(f"\n❌ Erro: O e-mail '{email}' já está em uso.")
            raise typer.Abort()

        password = getpass.getpass("Senha: ")
        password_confirm = getpass.getpass("Confirme a senha: ")

        if password != password_confirm:
            print("\n❌ Erro: As senhas não conferem.")
            raise typer.Abort()

        # Mostra as opções de perfil a partir do Enum
        perfil_str = typer.prompt(
            "Perfil do usuário", 
            type=typer.Choice([p.value for p in UserProfile]),
            default=UserProfile.ADVOGADO.value,
            show_choices=True
        )
        perfil = UserProfile(perfil_str)
        
        user_in = UserCreate(
            name=nome,
            email=email,
            password=password,
            profile=perfil,
        )
        
        user = user_service.create_user(db=db, user_in=user_in)
        
        print("\n--- ✅ Sucesso! ---")
        print(f"Usuário '{user.name}' criado com o e-mail '{user.email}' e perfil '{user.profile}'.")

    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    cli_app()