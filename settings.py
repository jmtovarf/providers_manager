import os
from distutils.util import strtobool
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

# App
PORT = int(os.getenv("PORT", 3000))
RELOAD = bool(strtobool(os.getenv("RELOAD", "True")))

# Database
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "adminpass")
DB_DATABASE = os.getenv("DB_DATABASE", "storedb")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)
