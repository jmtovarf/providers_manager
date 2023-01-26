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

    @classmethod
    def get_total(cls, db):
        return db.query(cls).count()

    @classmethod
    def get_all(cls, db, skip=0, limit=10):
        return db.query(cls).offset(skip).limit(limit).all()

    def update(self, db, data: dict):
        for key, value in data.items():
            setattr(self, key, value)

        db.add(self)
        db.commit()
        db.refresh(self)
        return self
