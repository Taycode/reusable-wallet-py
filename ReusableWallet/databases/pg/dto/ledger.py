from typing import Optional

from dataclasses import dataclass, asdict

from ReusableWallet.databases.pg.enums import ClerkType, TransactionType


@dataclass
class CreateLedgerDTO:
    asset_id: str
    clerk_type: ClerkType
    # ToDo: Transaction type should be dynamic
    entry_type: TransactionType
    transaction_id: str
    pending_balance: Optional[float] = 0
    pending_delta: Optional[float] = 0
    available_balance: Optional[float] = 0
    available_delta: Optional[float] = 0

    def to_dict(self):
        return asdict(self)


@dataclass
class LedgerBalance:
    pending_balance: float
    available_balance: float
