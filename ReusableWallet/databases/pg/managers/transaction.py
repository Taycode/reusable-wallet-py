from sqlalchemy.orm import Session

from ReusableWallet.databases.pg.dto.transaction import CreateTransactionDTO
from ReusableWallet.databases.pg.enums import TransactionStatus
from ReusableWallet.databases.pg.schema import Transaction


class TransactionManager:
    @staticmethod
    def create_transaction(payload: CreateTransactionDTO, session: Session):
        new_transaction = Transaction(**payload.to_dict())
        session.add(new_transaction)
        session.flush()
        return new_transaction

    @staticmethod
    def fetch_transactions(asset_id: str, session: Session):
        fetched_transactions = session.query(Transaction).filter(Transaction.asset == asset_id).all()
        return fetched_transactions

    @staticmethod
    def update_transaction(transaction_id: str, status: TransactionStatus, session: Session):
        fetched_transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()
        fetched_transaction.status = status
        return fetched_transaction

    @staticmethod
    def fetch_transaction_by_id(transaction_id: str, session: Session) -> Transaction:
        fetched_transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()
        return fetched_transaction
