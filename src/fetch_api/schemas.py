from typing import Optional

from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    id: Optional[int]
    user_id: int = Field(..., ge=1, alias="userId")
    title: str = Field(..., max_length=127)
    body: str = Field(..., max_length=255)

    class Config:
        from_attributes = True
