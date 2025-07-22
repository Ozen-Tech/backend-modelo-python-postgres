import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base_class import Base
from app.schemas.user import UserProfile
from sqlalchemy.orm import relationship  



class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    profile = Column(SQLAlchemyEnum(UserProfile), nullable=False, default=UserProfile.ADVOGADO)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    deadlines = relationship("Deadline", back_populates="responsible")