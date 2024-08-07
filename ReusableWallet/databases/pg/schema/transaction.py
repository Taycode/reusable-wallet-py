from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ReusableWallet.databases.pg.enums import TransactionStatus, ClerkType, TransactionType

from .base import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user = Column(String, nullable=False)  # Assuming there is a 'users' table
    asset_id = Column(UUID(as_uuid=True), ForeignKey('assets.id'), nullable=False)  # Assuming there is an 'assets' table
    symbol = Column(String, nullable=False)
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING)
    amount = Column(Float, nullable=False)  # Using Float to represent Decimal128
    fee = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    clerk_type = Column(SQLEnum(ClerkType), nullable=False)
    type = Column(SQLEnum(TransactionType), nullable=False)
    reason = Column(String, nullable=True)
    description = Column(String)
    metadata_ = Column("metadata", String)  # Store as JSON string or use JSONB for PostgreSQL

    # Additional fields for timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    asset = relationship("Asset", back_populates="transactions")
    ledgers = relationship("Ledger", back_populates="transactions")
