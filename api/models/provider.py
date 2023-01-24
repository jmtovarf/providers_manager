from sqlalchemy import Column, String, DateTime

from api.config.database import Base


class Provider(Base):
    __tablename__ = "provider"

    nit = Column(String(11), primary_key=True, index=True)
    name = Column(String(50), index=True)
    contact_name = Column(String(50), nullable=False)
    contact_number = Column(String(50), nullable=False)

    created_time = Column(DateTime, nullable=False)
    modified_time = Column(DateTime, nullable=False)
