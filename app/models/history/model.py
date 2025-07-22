# app/models/history/model.py
import uuid
from sqlalchemy import Column, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base_class import Base

class DeadlineHistory(Base):
    __tablename__ = "deadline_history"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_description = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deadline_id = Column(UUID(as_uuid=True), ForeignKey("deadlines.id"), nullable=False)
    acting_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    deadline = relationship("Deadline", back_populates="history")
    acting_user = relationship("User")