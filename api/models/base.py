from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr


class MixinModel:
    """Database common model"""

    @declared_attr
    def id(self):
        return Column("id", Integer, primary_key=True)

    # id = Column(Integer, primary_key=True)
    created_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def get_by_id(cls, db, id):
        return db.query(cls).filter_by(id=id).one_or_none()
