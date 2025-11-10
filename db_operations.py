from extensions import db
from models import User, Cryptocurrency, MarketPrice, Wallet, Orders, Transaction, Watchlist
from sqlalchemy import func

def get_all_users():
    return User.query.order_by(User.UserID).all()

def get_all_cryptos():
    return Cryptocurrency.query.order_by(Cryptocurrency.Name).all()

def get_user_wallet(user_id):
    return Wallet.query.filter_by(UserID=user_id).all()

def get_user_orders(user_id):
    return Orders.query.filter_by(UserID=user_id).order_by(Orders.Timestamp.desc()).all()

def get_user_transactions(user_id):
    return Transaction.query.filter_by(UserID=user_id).order_by(Transaction.Timestamp.desc()).all()

def add_order(user_id, crypto_id, order_type, quantity, price, status='Completed'):
    # Create order in Orders table.
    order = Orders(
        UserID=user_id,
        CryptoID=crypto_id,
        OrderType=order_type.upper(),
        Quantity=quantity,
        Price=price,
        Status=status
    )
    db.session.add(order)
    db.session.flush()  # get OrderID assigned if DB auto-increments
    # If your DB trigger inserts Transaction automatically, you may not need to create it here.
    # Otherwise, create a Transaction record here:
    # txn = Transaction(OrderID=order.OrderID, UserID=user_id, Amount=quantity*price, TransactionType='Trade')
    # db.session.add(txn)
    db.session.commit()
    return order

def get_portfolio_values():
    # Sum Wallet.Balance * MarketPrice.Price grouped by User
    q = db.session.query(
        User.Name,
        func.sum(Wallet.Balance * MarketPrice.Price).label('Portfolio_Value')
    ).join(Wallet, User.UserID == Wallet.UserID)\
     .join(MarketPrice, Wallet.CryptoID == MarketPrice.CryptoID)\
     .group_by(User.UserID).all()
    return q
