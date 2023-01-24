import re

from datetime import datetime
from pydantic import BaseModel, validator, Field
from typing import Optional

from api import _l
from api.schemas.account import AccountCreate


class ProviderBase(BaseModel):
    name: str = Field(..., description="Provider Name")
    nit: str = Field(max_length=11, description="Provider NIT")
    contact_name: str = Field(..., description="Provider Contact Name")
    contact_number: Optional[str] = Field(
        ..., description="Provider Contact Number (Optional)"
    )


class ProviderCreate(ProviderBase):
    account: AccountCreate = Field(..., description="Provider Account information")

    @validator("nit", pre=True)
    def nit_validation(cls, value):
        if not re.match(r"^\d{9}-?\d{0,1}$", value):
            raise ValueError(_l.get("invalid_nit_format"))
        return value


class Provider(ProviderCreate):
    created_time: datetime = Field(..., description="Time of provider creation")
    modified_time: datetime = Field(..., description="Time of provider update")

    class Config:
        schema_extra = {
            "example": {
                "name": "Acme Inc",
                "nit": "901362343-4",
                "contact_name": "John Doe",
                "contact_number": "5551234567",
                "account": {
                    "bank_name": "Acme Bank",
                    "account_number": "1234567890",
                },
            }
        }
