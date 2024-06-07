from sqlalchemy.orm import Session

from ReusableWallet.databases.pg.dto.transaction import CreateTransactionDTO
from ReusableWallet.databases.pg.enums import TransactionStatus
from ReusableWallet.databases.pg.schema import Transaction


class TransactionManager:
    @staticmethod
    def create_transaction(payload: CreateTransactionDTO, session: Session = None):
        close_session = session is None
        session = session or Session()
        new_transaction = Transaction(payload)
        session.add(new_transaction)
        if close_session:
            session.commit()
            session.close()
        return new_transaction

    @staticmethod
    def fetch_transactions(asset_id: str, session: Session = None):
        close_session = session is None
        session = session or Session()
        fetched_transactions = session.query(Transaction).filter(Transaction.asset == asset_id).all()
        if close_session:
            session.commit()
            session.close()
        return fetched_transactions

    @staticmethod
    def update_transaction(transaction_id: str, status: TransactionStatus, session: Session = None):
        close_session = session is None
        session = session or Session()
        fetched_transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()
        fetched_transaction.status = status
        if close_session:
            session.commit()
            session.close()
        return fetched_transaction
