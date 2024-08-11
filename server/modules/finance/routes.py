from fastapi import APIRouter, Depends
import server.modules.finance.service as finance_service
from server.modules.finance.schemas import FundWalletSchema, ConfirmFundWalletSchema
from server.modules.user import models as user_models, auth

router = APIRouter(prefix='/wallets')


@router.post("/fund")
def fund_wallet_route(payload: FundWalletSchema, user: user_models.User = Depends(auth.get_current_user)):
    finance_service.fund_user_wallet(user, payload.amount)


@router.post("/fund/confirm")
def confirm_fund_wallet_route(payload: ConfirmFundWalletSchema, user: user_models.User = Depends(auth.get_current_user)):
    finance_service.confirm_fund_user_wallet(payload.transaction_id)


@router.post("/withdraw")
def withdraw_from_wallet_route(payload: FundWalletSchema, user: user_models.User = Depends(auth.get_current_user)):
    finance_service.withdraw_from_user_waller(user, payload.amount)


@router.post("/withdraw/confirm")
def confirm_withdraw_from_wallet_route(payload: ConfirmFundWalletSchema, user: user_models.User = Depends(auth.get_current_user)):
    finance_service.confirm_withdraw_from_user_wallet(payload.transaction_id)


@router.post("/reverse")
def reverse_withdraw_wallet_route(payload: ConfirmFundWalletSchema, user: user_models.User = Depends(auth.get_current_user)):
    finance_service.reverse_withdrawal_from_user_wallet(payload.transaction_id)


@router.get("/transactions")
def fetch_transactions_route(user: user_models.User = Depends(auth.get_current_user)):
    return finance_service.fetch_transactions(user)


@router.get("/ledgers")
def fetch_ledgers_route(user: user_models.User = Depends(auth.get_current_user)):
    return finance_service.fetch_ledger(user)


@router.get("/balance")
def fetch_balance_route(user: user_models.User = Depends(auth.get_current_user)):
    return finance_service.fetch_balance(user)
