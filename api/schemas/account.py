from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


# Bank Serializers
class BankBase(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="Name of the bank")


class BankCreate(BankBase):
    pass


class Bank(BankBase):
    id: int = Field(..., description="Bank Id")
    created_time: datetime = Field(..., description="Time of bank creation")
    modified_time: datetime = Field(..., description="Time of bank update")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Acme Bank",
                "created_time": "2022-01-01 00:00:00",
                "modified_time": "2022-02-01 00:00:00",
            }
        }


# Providers Accounts
class AccountBase(BaseModel):
    account_number: Optional[str] = Field(
        default=None, min_length=1, max_length=15, description="Number of bank account"
    )


class AccountCreate(AccountBase):
    bank_id: Optional[int] = Field(
        default=None, description="Id of the bank related to the provider account"
    )

    bank_name: str = Field(
        ..., description="Name of the bank related to the provider account"
    )


class Account(AccountBase):
    id: int = Field(..., description="Account Id")
    bank: Bank = Field(..., description="Bank information")
    created_time: datetime = Field(..., description="Time of account creation")
    modified_time: datetime = Field(..., description="Time of account update")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "account_number": "1234567890",
                "bank": Bank.Config.schema_extra["example"],
                "created_time": "2022-01-01 00:00:00",
                "modified_time": "2022-02-01 00:00:00",
            }
        }
