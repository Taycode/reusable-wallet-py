from sqlalchemy import create_engine, Column, String, Float, ForeignKey, DateTime, Enum as SQLEnum, func
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ReusableWallet.databases.pg.enums import TransactionType, ClerkType
from .base import Base


class Ledger(Base):
    __tablename__ = 'ledgers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset = Column(String, ForeignKey('assets.id'), nullable=False, index=True)
    clerk_type = Column(SQLEnum(ClerkType), nullable=False)
    entry_type = Column(SQLEnum(TransactionType), nullable=False)
    transaction = Column(String, ForeignKey('transactions.id'), nullable=False, index=True)
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


# Assuming the Asset and Transaction models are defined with back_populates
class Asset(Base):
    __tablename__ = 'assets'
    name = Column(String, primary_key=True)
    ledgers = relationship("Ledger", back_populates="asset_details")


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(String, primary_key=True)
    ledgers = relationship("Ledger", back_populates="transaction_details")


# SQLAlchemy Engine Setup
DATABASE_URI = 'postgresql://your_username:your_password@localhost:5432/your_database'
engine = create_engine(DATABASE_URI, echo=True)

# Create all tables in the database
Base.metadata.create_all(engine)

# Example of creating a session and adding a new ledger entry
if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()

    new_ledger = Ledger(
        asset='Bitcoin',
        clerk_type='ClerkTypeExample',
        entry_type='TransactionTypeExample',
        transaction='TransactionID123',
        pending_balance=1000.0,
        pending_delta=50.0,
        available_balance=950.0,
        available_delta=-50.0
    )

    session.add(new_ledger)
    session.commit()
    session.close()
