from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DatabaseManager:

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(
            database_url
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Generator:
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


db_manager: Optional[DatabaseManager] = None


def get_db() -> Generator:
    if db_manager is None:
        raise RuntimeError("Database not initialized")
    yield from db_manager.get_session()
