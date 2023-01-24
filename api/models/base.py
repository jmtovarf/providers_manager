from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr

from api.config.database import Base


class MixinModel:
    """Database common model"""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_time = Column(DateTime, nullable=False)
    modified_time = Column(DateTime, nullable=False)

    @classmethod
    def get_by_id(cls, id: str):
        return cls.query.filter_by(id=id).one_or_none()
