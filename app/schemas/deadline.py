import uuid
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum
from .user import UserPublic
from .history import DeadlineHistoryPublic 

class DeadlineStatus(str, Enum):
    PENDENTE = "pendente"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"

class DeadlineClassification(str, Enum):
    NORMAL = "normal"
    CRITICO = "critico"
    FATAL = "fatal"

class DeadlineBase(BaseModel):
    task_description: str = Field(..., min_length=5)
    due_date: datetime
    process_number: str | None = None
    parties: str | None = None
    status: DeadlineStatus = DeadlineStatus.PENDENTE
    responsible_user_id: uuid.UUID | None = None

class DeadlineCreate(DeadlineBase):
    pass

class DeadlineUpdate(BaseModel):
    task_description: str | None = None
    due_date: datetime | None = None
    process_number: str | None = None
    parties: str | None = None
    status: DeadlineStatus | None = None
    responsible_user_id: uuid.UUID | None = None

# Schema principal, que será retornado pela API
class DeadlinePublic(DeadlineBase):
    id: uuid.UUID
    classification: DeadlineClassification
    responsible: UserPublic | None = None
    history: list[DeadlineHistoryPublic] = [] # Descomente quando o schema de histórico for criado
    created_at: datetime
    updated_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)