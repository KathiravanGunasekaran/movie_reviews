from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote

user = ""
password = quote("")
db = ""
server = ""

database_url = f"postgresql://{user}:{password}@{server}/{db}"
engine = create_engine(database_url)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()


def get_db():
    db_session = local_session()  # creating an instance of local session
    try:
        yield db_session  # returns db instance
    finally:
        db_session.close()  # close the connection after each request from client
