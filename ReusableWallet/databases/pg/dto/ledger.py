from typing import Optional

from dataclasses import dataclass

from ReusableWallet.databases.pg.enums import ClerkType, TransactionType


@dataclass
class CreateLedgerDTO:
    asset: str
    clerk_type: ClerkType
    # ToDo: Transaction type should be dynamic
    entry_type: TransactionType
    transaction: str
    pending_balance: Optional[float] = 0
    pending_delta: Optional[float] = 0
    available_balance: Optional[float] = 0
    available_delta: Optional[float] = 0


@dataclass
class LedgerBalance:
    pending_balance: float
    available_balance: float
