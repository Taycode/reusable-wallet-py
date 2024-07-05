from typing import Dict, Any

from sqlalchemy.orm import Session, sessionmaker

from ReusableWallet.databases.pg.dto.ledger import LedgerBalance, CreateLedgerDTO
from ReusableWallet.databases.pg.dto.transaction import CreateTransactionDTO
from ReusableWallet.databases.pg.enums import ClerkType, TransactionType, TransactionStatus
from ReusableWallet.databases.pg.managers.asset import AssetManager
from ReusableWallet.databases.pg.managers.transaction import TransactionManager
from ReusableWallet.databases.pg.managers.ledger import LedgerManager


class PgWallet:
    _db_initialized = False  # Class variable to ensure DB setup happens only once

    def __init__(self, uri: str):
        self.asset_manager = AssetManager
        self.transaction_manager = TransactionManager
        self.ledger_manager = LedgerManager
        if not PgWallet._db_initialized:
            self.engine = self.setup_database(uri)
            self.Session = sessionmaker(bind=self.engine)
            PgWallet._db_initialized = True

    @classmethod
    def setup_database(cls, uri: str):
        from sqlalchemy import create_engine
        from ReusableWallet.databases.pg.schema.base import Base

        engine = create_engine(uri)
        Base.metadata.create_all(engine)
        return engine

    def get_engine_instance(self):
        return self.engine

    def create_asset(self, session: Session, user_id: str, symbol: str):
        asset = self.asset_manager.create_asset(user_id, symbol, session)
        session.commit()
        return asset

    def fetch_user_asset(self, session: Session, user_id: str, symbol: str):
        return self.asset_manager.fetch_user_asset(user_id, symbol, session)

    def fetch_balance(self, session: Session, asset_id: str) -> LedgerBalance:
        last_ledger = self.ledger_manager.fetch_last_ledger(asset_id, session)
        return LedgerBalance(
            pending_balance=last_ledger.pending_balance,
            available_balance=last_ledger.available_balance
        )

    def initiate_fund_asset(
            self,
            session: Session,
            asset_id: str,
            amount: float,
            fee: float = 0,
            reason: str = None,
            description: str = None,
            metadata: Dict[str, Any] = None,
    ):
        # Fetch the asset and ensure it is attached to the session
        asset = self.asset_manager.fetch_asset_by_id(asset_id, session)
        if not asset:
            raise ValueError(f"Asset with id {asset_id} not found")
        create_transaction_payload = CreateTransactionDTO(
            user=asset.user,
            asset_id=asset.id,
            symbol=asset.symbol,
            amount=amount,
            fee=fee,
            total_amount=fee + amount,
            clerk_type=ClerkType.CREDIT,
            type=TransactionType.WALLET_FUND,
            reason=reason,
            description=description,
            metadata=metadata,
        )
        transaction = self.transaction_manager.create_transaction(create_transaction_payload, session)
        last_ledger = self.ledger_manager.fetch_last_ledger(asset.id, session)
        pending_balance = last_ledger.pending_balance if last_ledger else 0
        available_balance = last_ledger.available_balance if last_ledger else 0
        create_ledger_payload = CreateLedgerDTO(
            asset_id=asset.id,
            clerk_type=ClerkType.CREDIT,
            entry_type=TransactionType.WALLET_FUND,
            transaction_id=transaction.id,
            pending_balance=pending_balance + amount,
            pending_delta=amount,
            available_delta=0,
            available_balance=available_balance
        )
        ledger = self.ledger_manager.create_ledger(create_ledger_payload, session)
        session.commit()
        return ledger

    def validate_fund_asset(self, session: Session, transaction_id: str):
        # ToDo: verify logic
        transaction = self.transaction_manager.fetch_transaction_by_id(transaction_id, session)
        if transaction.type is not TransactionType.WALLET_FUND:
            raise Exception('Transaction is not a withdrawal')
        asset = self.asset_manager.fetch_asset_by_id(transaction.asset.id, session)
        last_ledger = self.ledger_manager.fetch_last_ledger(asset.id, session)
        pending_balance = last_ledger.pending_balance if last_ledger else 0
        available_balance = last_ledger.available_balance if last_ledger else 0
        create_ledger_payload = CreateLedgerDTO(
            asset_id=asset.id,
            clerk_type=ClerkType.CREDIT,
            entry_type=TransactionType.WALLET_FUND,
            transaction_id=transaction.id,
            available_balance=available_balance + transaction.amount,
            available_delta=transaction.amount,
            pending_delta=0,
            pending_balance=pending_balance
        )
        ledger = self.ledger_manager.create_ledger(create_ledger_payload, session)
        self.transaction_manager.update_transaction(transaction_id, TransactionStatus.SUCCESSFUL, session)
        session.commit()
        return ledger

    def initiate_charge_asset(
            self,
            session: Session,
            asset_id: str,
            amount: float,
            fee: float = 0,
            reason: str = None,
            description: str = None,
            metadata: Dict[str, Any] = None,
    ):
        # TodO: Use transaction, prevent anyone from reading the ledger to prevent race condition
        asset = self.asset_manager.fetch_asset_by_id(asset_id, session)
        if not asset:
            raise ValueError(f"Asset with id {asset_id} not found")
        last_ledger = self.ledger_manager.fetch_last_ledger(asset.id, session)
        pending_balance = last_ledger.pending_balance if last_ledger else 0
        available_balance = last_ledger.available_balance if last_ledger else 0
        if amount > available_balance:
            raise Exception("Insufficient balance")
        create_transaction_payload = CreateTransactionDTO(
            user=asset.user,
            asset_id=asset.id,
            symbol=asset.symbol,
            amount=amount,
            fee=fee,
            total_amount=fee + amount,
            clerk_type=ClerkType.DEBIT,
            type=TransactionType.WITHDRAWAL,
            reason=reason,
            description=description,
            metadata=metadata,
        )
        transaction = self.transaction_manager.create_transaction(create_transaction_payload, session)
        create_ledger_payload = CreateLedgerDTO(
            asset_id=asset.id,
            clerk_type=ClerkType.DEBIT,
            entry_type=TransactionType.WITHDRAWAL,
            transaction_id=transaction.id,
            available_balance=available_balance - amount,
            available_delta=-amount,
            pending_balance=pending_balance,
            pending_delta=0,
        )
        ledger = self.ledger_manager.create_ledger(create_ledger_payload, session)
        session.commit()
        return ledger

    def validate_charge_asset(self, session: Session, transaction_id: str):
        # ToDo: verify logic
        transaction = self.transaction_manager.fetch_transaction_by_id(transaction_id, session)
        if transaction.type is not TransactionType.WITHDRAWAL:
            raise Exception('Transaction is not a withdrawal')
        asset = self.asset_manager.fetch_asset_by_id(transaction.asset_id, session)
        last_ledger = self.ledger_manager.fetch_last_ledger(asset.id, session)
        pending_balance = last_ledger.pending_balance if last_ledger else 0
        available_balance = last_ledger.available_balance if last_ledger else 0
        create_ledger_payload = CreateLedgerDTO(
            asset_id=asset.id,
            clerk_type=ClerkType.DEBIT,
            entry_type=TransactionType.WITHDRAWAL,
            transaction_id=transaction.id,
            pending_balance=pending_balance - transaction.amount,
            pending_delta=-transaction.amount,
            available_balance=available_balance,
            available_delta=0
        )
        ledger = self.ledger_manager.create_ledger(create_ledger_payload, session)
        self.transaction_manager.update_transaction(transaction_id, TransactionStatus.SUCCESSFUL, session)
        session.commit()
        return ledger

    def reverse_charge_asset(
            self,
            session: Session,
            transaction_id: str,
            amount: float,
            fee: float,
            reason: str = None,
            description: str = None,
            metadata: Dict[str, Any] = None,
    ):
        # TodO: Use transaction, prevent anyone from reading the ledger to prevent race condition
        # ToDo: Use decrement and increment for the figures
        transaction = self.transaction_manager.fetch_transaction_by_id(transaction_id, session)
        if transaction.type is not TransactionType.WITHDRAWAL:
            raise Exception('Transaction is not a withdrawal')
        asset = self.asset_manager.fetch_asset_by_id(transaction.asset, session)
        last_ledger = self.ledger_manager.fetch_last_ledger(asset.id, session)
        pending_balance = last_ledger.pending_balance if last_ledger else 0
        available_balance = last_ledger.available_balance if last_ledger else 0
        create_transaction_payload = CreateTransactionDTO(
            user=asset.user,
            asset_id=asset.id,
            symbol=asset.symbol,
            amount=amount,
            fee=fee,
            total_amount=fee + amount,
            clerk_type=ClerkType.CREDIT,
            type=TransactionType.WITHDRAWAL_REVERSAL,
            reason=reason,
            description=description,
            metadata=metadata,
        )
        transaction = self.transaction_manager.create_transaction(create_transaction_payload, session)
        create_ledger_payload = CreateLedgerDTO(
            asset_id=asset.id,
            clerk_type=ClerkType.CREDIT,
            entry_type=TransactionType.WITHDRAWAL_REVERSAL,
            transaction_id=transaction.id,
            available_balance=available_balance + amount,
            available_delta=amount,
            pending_delta=0,
            pending_balance=pending_balance,
        )
        ledger = self.ledger_manager.create_ledger(create_ledger_payload, session)
        session.commit()
        return ledger
