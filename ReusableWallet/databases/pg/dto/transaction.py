from typing import Optional, Any, Dict

from dataclasses import dataclass, asdict

from ReusableWallet.databases.pg.enums import TransactionStatus, ClerkType, TransactionType
from ReusableWallet.databases.pg.schema import Asset


@dataclass
class CreateTransactionDTO:
    user: str
    asset_id: str
    symbol: str
    amount: float
    fee: float
    total_amount: float
    clerk_type: ClerkType
    type: TransactionType
    reason: str
    description: Optional[str]
    metadata: Dict[str, Any]
    status: TransactionStatus = TransactionStatus.PENDING

    def to_dict(self):
        return asdict(self)
