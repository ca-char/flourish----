
import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_for_dev")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "db")
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_NAME}'
    LOAD_SAMPLE_DATA = os.getenv("LOAD_SAMPLE_DATA", "False") == "True"
    # True for first-time use