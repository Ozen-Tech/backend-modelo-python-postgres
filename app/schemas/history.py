import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Any
from .user import UserPublic

class DeadlineHistoryPublic(BaseModel):
    id: uuid.UUID
    action_description: str
    details: dict[str, Any] | None = None
    created_at: datetime
    acting_user: UserPublic
    model_config = ConfigDict(from_attributes=True)