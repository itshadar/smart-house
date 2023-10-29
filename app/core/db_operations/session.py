from sqlalchemy.orm import Session
from sqlalchemy.engine import create_engine
from config import database_uri

engine = create_engine(database_uri, echo=True)


def get_session() -> Session:
    return Session(engine)
