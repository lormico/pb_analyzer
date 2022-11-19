from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


def get_db_session(db_file_path):
    engine = create_engine(f"sqlite:///{db_file_path}")
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()
