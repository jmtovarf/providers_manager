from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from api.config.database import Base
from api.models.base import MixinModel


class Bank(MixinModel, Base):
    __tablename__ = "bank"

    name = Column(String(50), unique=True, index=True)

    @classmethod
    def create(cls, db, bank):
        bank = cls(**bank.dict())
        db.add(bank)
        db.commit()
        db.refresh(bank)
        return bank


class Account(MixinModel, Base):
    __tablename__ = "account"

    account_number = Column(String(15), unique=True, index=True)

    # Bank Information
    bank_id = Column(Integer, ForeignKey("bank.id"))
    bank = relationship("Bank")

    # Provider Information
    provider_id = Column(String(11), ForeignKey("provider.nit"))
    provider = relationship("Provider")
