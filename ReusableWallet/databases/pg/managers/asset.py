from sqlalchemy.orm import Session

from ReusableWallet.databases.pg.schema import Asset


class AssetManager:
    @staticmethod
    def create_asset(user_id: str, symbol: str, session: Session):
        """Create and persist an asset using the provided SQLAlchemy session.

        Parameters:
        user_id (str): The user identifier for whom the asset is created.
        symbol (str): The symbol of the asset to be created.
        session (Session): An SQLAlchemy Session object.

        Returns:
        Asset: The created Asset object.
        """
        new_asset = Asset(user=user_id, symbol=symbol)
        session.add(new_asset)
        return new_asset

    @staticmethod
    def create_asset_with_commit(user_id: str, symbol: str):
        """Create an asset and commit the transaction.

        This method creates a session, adds the new asset, commits the transaction,
        and then closes the session, handling all steps of the transaction lifecycle.

        Parameters:
        user_id (str): The user identifier for whom the asset is created.
        symbol (str): The symbol of the asset to be created.

        Returns:
        Asset: The created Asset object.
        """
        with Session() as session:
            new_asset = AssetManager.create_asset(user_id, symbol, session)
            session.commit()
            return new_asset

    @staticmethod
    def fetch_user_asset(user_id: str, symbol: str):
        """Fetch a user asset

        Parameters:
            user_id (str): The user identifier for whom the asset belongs to
            symbol (str): The symbol of the asset

        Returns:
            Asset: The fetched Asset Object
        """
        with Session() as session:
            fetched_asset = session.query(Asset).filter(Asset.user == user_id).filter(Asset.symbol == symbol).first()
            return fetched_asset

    @staticmethod
    def fetch_user_asset_with_transaction(user_id: str, symbol: str, session: Session):
        """Fetch a user asset

        Parameters:
            user_id (str): The user identifier for whom the asset belongs to
            symbol (str): The symbol of the asset
            session (Session): Transaction session

        Returns:
            Asset: The fetched Asset Object
        """
        return session.query(Asset).filter(Asset.user == user_id).filter(Asset.symbol == symbol).first()
