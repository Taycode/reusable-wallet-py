from server.modules.user.models import User
from server.wallet import wallet


def create_asset(user: User):
    with wallet.Session() as session:
        asset = wallet.create_asset(session, user.id, 'NGN')
        return asset


def fund_user_wallet(user: User, amount: float):
    with wallet.Session() as session:
        asset = wallet.fetch_user_asset(session, user.id, 'NGN')
        wallet.initiate_fund_asset(session, asset.id, amount)


def confirm_fund_user_wallet(transaction_id: str):
    with wallet.Session() as session:
        wallet.validate_fund_asset(session, transaction_id)


def withdraw_from_user_waller(user: User, amount: float):
    with wallet.Session() as session:
        asset = wallet.fetch_user_asset(session, user.id, 'NGN')
        wallet.initiate_charge_asset(session, asset.id, amount)


def confirm_withdraw_from_user_wallet(transaction_id: str):
    with wallet.Session() as session:
        wallet.validate_charge_asset(session, transaction_id)


def reverse_withdrawal_from_user_wallet(transaction_id: str):
    with wallet.Session() as session:
        wallet.reverse_charge_asset(session, transaction_id)


def fetch_transactions(user: User):
    with wallet.Session() as session:
        asset = wallet.fetch_user_asset(session, user.id, 'NGN')
        return wallet.fetch_transactions(session, asset.id)


def fetch_ledger(user: User):
    with wallet.Session() as session:
        asset = wallet.fetch_user_asset(session, user.id, 'NGN')
        return wallet.fetch_ledger(session, asset.id)


def fetch_balance(user: User):
    with wallet.Session() as session:
        asset = wallet.fetch_user_asset(session, user)
        return wallet.fetch_balance(session, asset.id)
