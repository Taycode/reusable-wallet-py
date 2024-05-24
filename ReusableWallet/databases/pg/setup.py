from sqlalchemy import create_engine

from ReusableWallet.databases.pg.schema.base import Base


def setup_database(uri: str) -> None:
    engine = create_engine(uri)
    Base.metadata.create_all(engine)
