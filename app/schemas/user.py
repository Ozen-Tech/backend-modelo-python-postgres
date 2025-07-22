import uuid
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum

class UserProfile(str, Enum):
    ADMIN = "admin"
    ADVOGADO = "advogado"
    ESTAGIARIO = "estagiario"

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=3)
    profile: UserProfile = UserProfile.ADVOGADO

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserPublic(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    profile: UserProfile
    model_config = ConfigDict(from_attributes=True)