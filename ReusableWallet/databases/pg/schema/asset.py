from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ReusableWallet.databases.pg.enums import ActivityStatus
from .base import Base


class Asset(Base):
    __tablename__ = 'assets'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, nullable=False)
    user = Column(String, nullable=False)  # Assuming there is a 'users' table
    withdrawal_activity = Column(SQLEnum(ActivityStatus), default=ActivityStatus.ACTIVE)
    # Relationship - Assuming Ledger has an asset_id foreign key linking to Asset
    ledgers = relationship("Ledger", back_populates="asset")
    transactions = relationship("Transaction", back_populates="asset")

    # Setting up a unique constraint on user and symbol
    __table_args__ = (UniqueConstraint('user', 'symbol', name='_user_symbol_uc'),)

    # Relationships can be defined if needed
    # user_details = relationship("User", back_populates="assets")

    # Automatic timestamp handling
    created_at = Column(String, default=func.now())
    updated_at = Column(String, default=func.now(), onupdate=func.now())

# Example of User class, if needed
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(String, primary_key=True, default=uuid.uuid4)
#     assets = relationship("Asset", back_populates="user_details")
