from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from ReusableWallet.databases.pg.managers.asset import AssetManager
from ReusableWallet.databases.pg.schema import Asset


class Wallet(ABC, AssetManager):
    _db_initialized = False  # Class variable to ensure DB setup happens only once

    def __init__(self, uri: str):
        if not Wallet._db_initialized:
            self.setup_database(uri)
            Wallet._db_initialized = True

    @classmethod
    def setup_database(cls, uri: str):
        from sqlalchemy import create_engine
        from ReusableWallet.databases.pg.schema.base import Base

        engine = create_engine(uri)
        Base.metadata.create_all(engine)
