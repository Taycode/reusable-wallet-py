from sqlalchemy.orm import Session

from ReusableWallet.databases.pg.dto.ledger import CreateLedgerDTO
from ReusableWallet.databases.pg.schema import Ledger


class LedgerManager:
    @staticmethod
    def create_ledger(payload: CreateLedgerDTO, session: Session):
        new_ledger = Ledger(payload)


