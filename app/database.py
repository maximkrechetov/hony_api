from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from os import environ

db_user = environ.get('DB_USER')
db_name = environ.get('DB_NAME')
db_host = environ.get('DB_HOST')
db_password = environ.get('DB_PASSWORD')

db_url = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Yields db connection
    :return:
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
