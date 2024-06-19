from sqlalchemy.orm import Session
from ReusableWallet.databases.pg.schema import Asset


class AssetManager:
    @staticmethod
    def create_asset(user_id: str, symbol: str, session: Session = None) -> Asset:
        """Create and persist an asset.

        If a session is provided, it will use the session to add the asset.
        If no session is provided, it will create a session, add the asset,
        commit the transaction, and close the session.

        Parameters:
        user_id (str): The user identifier for whom the asset is created.
        symbol (str): The symbol of the asset to be created.
        session (Session, optional): An SQLAlchemy Session object.

        Returns:
        Asset: The created Asset object.
        """
        close_session = session is None
        session = session or Session()
        new_asset = Asset(user=user_id, symbol=symbol)
        session.add(new_asset)
        if close_session:
            session.commit()
            session.close()
        return new_asset

    @staticmethod
    def fetch_user_asset(user_id: str, symbol: str, session: Session = None) -> Asset:
        """Fetch a user asset.

        If a session is provided, it will use the session to fetch the asset.
        If no session is provided, it will create a session, fetch the asset,
        and close the session.

        Parameters:
        user_id (str): The user identifier for whom the asset belongs.
        symbol (str): The symbol of the asset.
        session (Session, optional): An SQLAlchemy Session object.

        Returns:
        Asset: The fetched Asset object.
        """
        close_session = session is None
        session = session or Session()
        fetched_asset = session.query(Asset).filter(Asset.user == user_id).filter(Asset.symbol == symbol).first()
        if close_session:
            session.commit()
            session.close()
        return fetched_asset

    @staticmethod
    def fetch_asset_by_id(asset_id: str, session: Session = None) -> Asset:
        """Fetch a user asset by id.

        If a session is provided, it will use the session to fetch the asset.
        If no session is provided, it will create a session, fetch the asset,
        and close the session.

        Parameters:
        asset_id (str): The asset identifier.
        session (Session, optional): An SQLAlchemy Session object.

        Returns:
        Asset: The fetched Asset object.
        """
        close_session = session is None
        session = session or Session()
        fetched_asset = session.query(Asset).filter(Asset.id == asset_id).first()
        if close_session:
            session.commit()
            session.close()
        return fetched_asset
