from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from api.config.database import Base
from api.models.base import MixinModel


class Bank(MixinModel, Base):
    __tablename__ = "bank"

    name = Column(String(50), unique=True, index=True)

    @classmethod
    def get_by_name(cls, db, name):
        return db.query(cls).filter_by(name=name).one_or_none()

    @classmethod
    def create(cls, db, bank):
        bank = cls(**bank.dict())
        db.add(bank)
        db.commit()
        db.refresh(bank)
        return bank

    def __str__(self) -> str:
        return f"Bank ({self.name})"


class Account(MixinModel, Base):
    __tablename__ = "account"

    account_number = Column(String(15), unique=True, index=True)

    # Bank Information
    bank_id = Column(Integer, ForeignKey("bank.id"))
    bank = relationship("Bank")

    # Provider Information
    provider_id = Column(String(11), ForeignKey("provider.nit"))
    provider = relationship("Provider", backref=backref("account", uselist=False))

    @classmethod
    def create(cls, db, data):
        account = cls(**data)
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    def __str__(self) -> str:
        return f"Account ({self.id}) (Provider {self.provider_id})"
