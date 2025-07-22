import uuid
from sqlalchemy.orm import Session
from app.models.deadline.model import Deadline
from app.models.history.model import DeadlineHistory
from app.schemas.deadline import DeadlineCreate, DeadlineUpdate

def get_deadline_by_id(db: Session, deadline_id: uuid.UUID) -> Deadline | None:
    return db.query(Deadline).filter(Deadline.id == deadline_id).first()

def get_all_deadlines(db: Session, skip: int = 0, limit: int = 100) -> list[Deadline]:
    return db.query(Deadline).order_by(Deadline.due_date.asc()).offset(skip).limit(limit).all()

def create_deadline(db: Session, *, deadline_in: DeadlineCreate, user_id: uuid.UUID) -> Deadline:
    # Cria o objeto do prazo
    db_deadline = Deadline(**deadline_in.model_dump())
    db.add(db_deadline)
    db.flush() # Usa flush para obter o ID do novo prazo antes do commit final

    # Cria o registro de histórico de criação
    history_log = DeadlineHistory(
        deadline_id=db_deadline.id,
        acting_user_id=user_id,
        action_description="Prazo criado.",
        details=deadline_in.model_dump(mode="json")
    )
    db.add(history_log)
    
    db.commit()
    db.refresh(db_deadline)
    return db_deadline

def update_deadline(
    db: Session, *, db_obj: Deadline, obj_in: DeadlineUpdate, user_id: uuid.UUID
) -> Deadline:
    update_data = obj_in.model_dump(exclude_unset=True)
    history_details = {}
    
    # Itera sobre os dados de atualização para construir o objeto de histórico
    for field, value in update_data.items():
        old_value = getattr(db_obj, field)
        if old_value != value:
            history_details[field] = {"de": str(old_value), "para": str(value)}
            setattr(db_obj, field, value)
    
    # Se houve alguma alteração, cria um log de histórico
    if history_details:
        history_log = DeadlineHistory(
            deadline_id=db_obj.id,
            acting_user_id=user_id,
            action_description="Prazo atualizado.",
            details=history_details,
        )
        db.add(history_log)
        
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_deadline(db: Session, *, db_obj: Deadline):
    # Aqui optamos pela exclusão física, mas uma exclusão lógica (mudar status) também é válida
    db.delete(db_obj)
    db.commit()
    return db_obj