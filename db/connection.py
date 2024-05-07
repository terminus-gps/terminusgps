from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from typing import Self
from terminusgps.config import TerminusGpsConfig

class DatabaseSession:
    def __init__(self) -> None:
        self.url = URL.create(
            drivername="postgresql",
            username=TerminusGpsConfig.DB_USER,
            host=TerminusGpsConfig.DB_HOST,
            database=TerminusGpsConfig.DB_NAME,
        )

        self.engine = create_engine(self.url)
        self.connection = self.engine.connect()

        return None

    def __enter__(self) -> Self:
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self

    def __exit__(self, a,b,c) -> None:
        return None

    @property
    def get_connection(self):
        return self.connection

    @property
    def get_engine(self):
        return self.engine
