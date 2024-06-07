from sqlalchemy.orm import Session

from ReusableWallet.databases.pg.dto.ledger import CreateLedgerDTO
from ReusableWallet.databases.pg.schema import Ledger


class LedgerManager:
    @staticmethod
    def create_ledger(payload: CreateLedgerDTO, session: Session = None) -> Ledger:
        close_session = session is None
        session = session or Session()
        new_ledger = Ledger(payload)
        session.add(new_ledger)
        if close_session:
            session.commit()
            session.close()
        return new_ledger

    @staticmethod
    def fetch_last_ledger(asset_id: str, session: Session = None) -> Ledger:
        close_session = session is None
        session = session or Session()
        fetched_ledger = session.query(Ledger).filter(Ledger.asset == asset_id).order_by(Ledger.created_at).first()
        if close_session:
            session.commit()
            session.close()
        return fetched_ledger
