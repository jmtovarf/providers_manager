from api.config.database import engine
from api.models.user import Base as BaseUser
from api.models.account import Base as BaseAccount
from api.models.provider import Base as BaseProvider


def create_db_models():
    BaseUser.metadata.create_all(bind=engine)
    BaseAccount.metadata.create_all(bind=engine)
    BaseProvider.metadata.create_all(bind=engine)
