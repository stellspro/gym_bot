import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from utils import config
from sqlalchemy.orm import sessionmaker


engine = sqlalchemy.create_engine(config.database_config.get_secret_value())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

Base = declarative_base()
