import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY=os.getenv("SECRET_KEY")
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_TIME_TOKEN_EXPIRES=timedelta(hours=1)
    SQLALCHEMY_ENGINE_OPTIONS={
        "pool_pre_ping":True,
        "pool_recycle":300
    }
class DevelopmentConfig(Config):
    Debug=True
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")
class ProductionConfig(Config):
    Debug=True
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")
config={
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}