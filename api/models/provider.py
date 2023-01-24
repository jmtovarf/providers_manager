from datetime import datetime
from sqlalchemy import Column, String, DateTime

from api.config.database import Base
from api.models.base import MixinModel


class Provider(MixinModel, Base):
    __tablename__ = "provider"

    id = Column("nit", String(11), primary_key=True, index=True)
    name = Column(String(50), index=True)
    contact_name = Column(String(50), nullable=False)
    contact_number = Column(String(50), nullable=False)
