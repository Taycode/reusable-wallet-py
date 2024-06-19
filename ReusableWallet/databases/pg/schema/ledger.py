from sqlalchemy import create_engine, Column, String, Float, ForeignKey, DateTime, Enum as SQLEnum, func
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ReusableWallet.databases.pg.enums import TransactionType, ClerkType
from .base import Base


class Ledger(Base):
    __tablename__ = 'ledgers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset = Column(UUID(as_uuid=True), ForeignKey('assets.id'), nullable=False, index=True)
    clerk_type = Column(SQLEnum(ClerkType), nullable=False)
    entry_type = Column(SQLEnum(TransactionType), nullable=False)
    transaction = Column(UUID(as_uuid=True), ForeignKey('transactions.id'), nullable=False, index=True)
    pending_balance = Column(Float, nullable=False, default=0)
    pending_delta = Column(Float, nullable=False, default=0)
    available_balance = Column(Float, nullable=False, default=0)
    available_delta = Column(Float, nullable=False, default=0)

    # Additional fields for timestamps
    created_at = Column(DateTime, default=func.now())

    # Define relationships (if other tables 'assets' and 'transactions' exist)
    asset_details = relationship("Asset", back_populates="ledgers")
    transaction_details = relationship("Transaction", back_populates="ledgers")

    # Use custom JSON serialization
    def to_dict(self):
        return {
            "id": str(self.id),
            "asset": self.asset,
            "clerk_type": self.clerk_type,
            "entry_type": self.entry_type,
            "transaction": self.transaction,
            "pending_balance": self.pending_balance,
            "pending_delta": self.pending_delta,
            "available_balance": self.available_balance,
            "available_delta": self.available_delta
        }
