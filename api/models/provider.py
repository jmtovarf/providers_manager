from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from api.config.database import Base
from api.models.base import MixinModel
from api.models.account import Account, Bank


class Provider(MixinModel, Base):
    __tablename__ = "provider"

    id = Column("nit", String(11), primary_key=True, index=True)
    name = Column(String(50), index=True)
    contact_name = Column(String(50), nullable=False)
    contact_number = Column(String(50), nullable=False)

    @property
    def nit(self):
        return self.id

    def update(self, db, data):
        provider_data = dict(
            id=data["nit"],
            name=data["name"],
            contact_name=data["contact_name"],
            contact_number=data["contact_number"],
        )
        super().update(db, data=provider_data)

        bank = self.account.bank
        if self.account.bank.name != data["bank_name"]:
            bank = Bank.get_by_name(db, name=data["bank_name"])

        account_data = dict(
            bank=bank,
            account_number=data["account_number"],
        )

        self.account.update(db, data=account_data)

        return self

    @classmethod
    def create(cls, db, data):
        # Create provider model
        provider_model = cls(
            id=data["nit"],
            name=data["name"],
            contact_name=data["contact_name"],
            contact_number=data["contact_number"],
        )

        db.add(provider_model)
        db.commit()
        db.refresh(provider_model)

        # Create account model
        bank = Bank.get_by_name(db, name=data["bank_name"])
        account_data = dict(
            provider_id=provider_model.id,
            bank=bank,
            account_number=data["account_number"],
        )
        account_model = Account.create(db, data=account_data)

        return provider_model, account_model

    def __str__(self) -> str:
        return f"Provider ({self.id}) {self.name}"
