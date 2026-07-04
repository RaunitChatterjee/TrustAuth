import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "trustauth-dev-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///../database/bank.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False