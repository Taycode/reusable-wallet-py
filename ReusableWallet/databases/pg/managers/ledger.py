from sqlalchemy import desc
from sqlalchemy.orm import Session

from ReusableWallet.databases.pg.dto.ledger import CreateLedgerDTO
from ReusableWallet.databases.pg.schema import Ledger


class LedgerManager:
    @staticmethod
    def create_ledger(payload: CreateLedgerDTO, session: Session) -> Ledger:
        new_ledger = Ledger(**payload.to_dict())
        session.add(new_ledger)
        return new_ledger

    @staticmethod
    def fetch_last_ledger(asset_id: str, session: Session) -> Ledger:
        fetched_ledger = (session.query(Ledger)
                          .filter(Ledger.asset_id == asset_id)
                          .order_by(desc(Ledger.created_at))
                          .first())
        return fetched_ledger
