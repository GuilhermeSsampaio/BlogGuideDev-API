from uuid import UUID
from datetime import datetime
from pydantic import EmailStr, BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
