from typing import Optional
from pydantic import BaseModel


class RegisterData(BaseModel):
    phone: str
    nickname: Optional[str] = None
    password: str
