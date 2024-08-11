from pydantic import BaseModel, Field


class FundWalletSchema(BaseModel):
    amount: float = Field(
        ...,
        description="Amount user wants to fund with"
    )


class ConfirmFundWalletSchema(BaseModel):
    transaction_id: str = Field(
        ...,
        description='Transaction ID to confirm',
    )
