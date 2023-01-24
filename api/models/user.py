from sqlalchemy import Column, String

from api.config.database import Base
from api.models.base import MixinModel


class User(MixinModel, Base):
    __tablename__ = "user"

    email = Column(String(250), unique=True, index=True)
    hashed_password = Column("password", String(50))
