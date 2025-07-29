
import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class NotificationPublic(BaseModel):
    id: uuid.UUID
    title: str
    body: str
    is_read: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)