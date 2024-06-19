from abc import ABC
from typing import Dict, Any

from sqlalchemy.orm import Session

from ReusableWallet.databases.pg.dto.ledger import LedgerBalance, CreateLedgerDTO
from ReusableWallet.databases.pg.dto.transaction import CreateTransactionDTO
from ReusableWallet.databases.pg.enums import ClerkType, TransactionType, TransactionStatus
from ReusableWallet.databases.pg.managers.asset import AssetManager
from ReusableWallet.databases.pg.managers.transaction import TransactionManager
from ReusableWallet.databases.pg.managers.ledger import LedgerManager


class PgWallet(ABC):
    _db_initialized = False  # Class variable to ensure DB setup happens only once

    def __init__(self, uri: str):
        self.asset_manager = AssetManager
        self.transaction_manager = TransactionManager
        self.ledger_manager = LedgerManager
        if not PgWallet._db_initialized:
            self.setup_database(uri)
            PgWallet._db_initialized = True

    @classmethod
    def setup_database(cls, uri: str):
        from sqlalchemy import create_engine
        from ReusableWallet.databases.pg.schema.base import Base

        engine = create_engine(uri)
        Base.metadata.create_all(engine)

    def create_asset(self, user_id: str, symbol: str):
        return self.asset_manager.create_asset(user_id, symbol)

    def fetch_user_asset(self, user_id: str, symbol: str):
        return self.asset_manager.fetch_user_asset(user_id, symbol)

    def fetch_balance(self, asset_id: str) -> LedgerBalance:
        last_ledger = self.ledger_manager.fetch_last_ledger(asset_id)
        return LedgerBalance(
            pending_balance=last_ledger.pending_balance,
            available_balance=last_ledger.available_balance
        )

    def initiate_fund_asset(
            self,
            asset_id: str,
            amount: float,
            fee: float,
            reason: str = None,
            description: str = None,
            metadata: Dict[str, Any] = None,
    ):
        # TodO: Use transaction, prevent anyone from reading the ledger to prevent race condition
        # ToDo: Use decrement and increment for the figures
        with Session() as session:
            asset = self.asset_manager.fetch_asset_by_id(asset_id, session)
            last_ledger = self.ledger_manager.fetch_last_ledger(asset.id)
            create_transaction_payload = CreateTransactionDTO(
                user=asset.user,
                asset=asset.id,
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
            transaction = self.transaction_manager.create_transaction(create_transaction_payload)
            create_ledger_payload = CreateLedgerDTO(
                asset=asset.id,
                clerk_type=ClerkType.CREDIT,
                entry_type=TransactionType.WALLET_FUND,
                transaction=transaction.id,
                pending_balance=last_ledger.pending_balance + amount,
                pending_delta=amount
            )
            ledger = self.ledger_manager.create_ledger(create_ledger_payload)
            return ledger

    def validate_fund_asset(self, transaction_id: str):
        with Session() as session:
            # ToDo: verify logic
            transaction = self.transaction_manager.fetch_transaction_by_id(transaction_id, session)
            asset = self.asset_manager.fetch_asset_by_id(transaction.asset, session)
            last_ledger = self.ledger_manager.fetch_last_ledger(asset.id, session)
            create_ledger_payload = CreateLedgerDTO(
                asset=asset.id,
                clerk_type=ClerkType.CREDIT,
                entry_type=TransactionType.WALLET_FUND,
                transaction=transaction.id,
                available_balance=last_ledger.available_balance + transaction.amount,
                available_delta=transaction.amount
            )
            ledger = self.ledger_manager.create_ledger(create_ledger_payload, session)
            self.transaction_manager.update_transaction(transaction_id, TransactionStatus.SUCCESSFUL)
            return ledger

    def initiate_charge_asset(
            self,
            asset_id: str,
            amount: float,
            fee: float,
            reason: str = None,
            description: str = None,
            metadata: Dict[str, Any] = None,
    ):
        # TodO: Use transaction, prevent anyone from reading the ledger to prevent race condition
        # ToDo: Use decrement and increment for the figures
        with Session() as session:
            asset = self.asset_manager.fetch_asset_by_id(asset_id, session)
            last_ledger = self.ledger_manager.fetch_last_ledger(asset.id)
            create_transaction_payload = CreateTransactionDTO(
                user=asset.user,
                asset=asset.id,
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
            transaction = self.transaction_manager.create_transaction(create_transaction_payload)
            create_ledger_payload = CreateLedgerDTO(
                asset=asset.id,
                clerk_type=ClerkType.DEBIT,
                entry_type=TransactionType.WITHDRAWAL,
                transaction=transaction.id,
                available_balance=last_ledger.available_balance - amount,
                available_delta=-amount
            )
            ledger = self.ledger_manager.create_ledger(create_ledger_payload)
            return ledger

    def validate_charge_asset(self, transaction_id: str):
        with Session() as session:
            # ToDo: verify logic
            transaction = self.transaction_manager.fetch_transaction_by_id(transaction_id, session)
            asset = self.asset_manager.fetch_asset_by_id(transaction.asset, session)
            last_ledger = self.ledger_manager.fetch_last_ledger(asset.id)
            create_ledger_payload = CreateLedgerDTO(
                asset=asset.id,
                clerk_type=ClerkType.DEBIT,
                entry_type=TransactionType.WITHDRAWAL,
                transaction=transaction.id,
                pending_balance=last_ledger.pending_balance - transaction.amount,
                pending_delta=-transaction.amount
            )
            ledger = self.ledger_manager.create_ledger(create_ledger_payload)
            self.transaction_manager.update_transaction(transaction_id, TransactionStatus.SUCCESSFUL)
            return ledger

    def reverse_charge_asset(
            self,
            transaction_id: str,
            amount: float,
            fee: float,
            reason: str = None,
            description: str = None,
            metadata: Dict[str, Any] = None,
    ):
        # TodO: Use transaction, prevent anyone from reading the ledger to prevent race condition
        # ToDo: Use decrement and increment for the figures
        with Session() as session:
            transaction = self.transaction_manager.fetch_transaction_by_id(transaction_id, session)
            asset = self.asset_manager.fetch_asset_by_id(transaction.asset, session)
            last_ledger = self.ledger_manager.fetch_last_ledger(asset.id)
            create_transaction_payload = CreateTransactionDTO(
                user=asset.user,
                asset=asset.id,
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
            transaction = self.transaction_manager.create_transaction(create_transaction_payload)
            create_ledger_payload = CreateLedgerDTO(
                asset=asset.id,
                clerk_type=ClerkType.CREDIT,
                entry_type=TransactionType.WITHDRAWAL_REVERSAL,
                transaction=transaction.id,
                available_balance=last_ledger.available_balance + amount,
                available_delta=amount
            )
            ledger = self.ledger_manager.create_ledger(create_ledger_payload)
            return ledger
