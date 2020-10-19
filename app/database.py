import databases
import sqlalchemy

from os import environ

db_user = environ.get('DB_USER')
db_name = environ.get('DB_NAME')
db_host = environ.get('DB_HOST')
db_password = environ.get('DB_PASSWORD')

db_url = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

metadata = sqlalchemy.MetaData()
db = databases.Database(db_url)

db_engine = sqlalchemy.create_engine(
    db_url,
    # connect_args={'check_same_thread': False}
)

metadata.create_all(db_engine)
