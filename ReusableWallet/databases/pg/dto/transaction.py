from typing import Optional, Any, Dict

from dataclasses import dataclass

from ReusableWallet.databases.pg.enums import TransactionStatus, ClerkType, TransactionType


@dataclass
class CreateTransactionDTO:
    user: str
    asset: str
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
