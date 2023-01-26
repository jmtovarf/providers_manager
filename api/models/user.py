from sqlalchemy import Column, String
from werkzeug.security import generate_password_hash, check_password_hash

from api.config.database import Base
from api.models.base import MixinModel


class User(MixinModel, Base):
    __tablename__ = "user"

    email = Column(String(250), unique=True, index=True)
    hashed_password = Column("password", String(250))

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @classmethod
    def get_by_email(cls, db, email: str):
        return db.query(cls).filter(cls.email == email).one_or_none()

    @classmethod
    def create(cls, db, user):
        db_user = cls(email=user.email)
        db_user.set_password(user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def __str__(self):
        return f"({self.id}) {self.email}"
