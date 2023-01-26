from pydantic import BaseModel, Field
from typing import Optional


class Pagination(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = 10


class MessageResponse(BaseModel):
    message: str = Field(..., description="Response message")
    redirect_to: Optional[str] = Field(
        default=None, description="Path to redirect to once request ends"
    )

    class Config:
        schema_extra = {
            "example": {
                "message": "success",
                "redirect_to": "/api/v1/login",
            }
        }
