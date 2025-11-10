from flask import Blueprint, render_template
from extensions import db
from models import User, Cryptocurrency, MarketPrice, Wallet, Orders, Transaction, Watchlist

bp = Blueprint('public', __name__)

# -------------------------------
# 🏠 Home Page — Redirects to login (handled in app.py)
# -------------------------------
# ⚠️ We intentionally removed @bp.route('/') to let app.py handle the root login redirect

# -------------------------------
# 💰 Show All Cryptocurrencies
# -------------------------------
@bp.route('/cryptos')
def cryptos():
    all_cryptos = Cryptocurrency.query.all()
    return render_template('index.html', cryptos=all_cryptos)

# -------------------------------
# 👥 All Users
# -------------------------------
@bp.route('/users')
def users():
    all_users = User.query.all()
    return render_template('user_list.html', users=all_users)

# -------------------------------
# 💼 Portfolio of all users
# -------------------------------
@bp.route('/portfolio')
def portfolio():
    portfolio_data = db.session.query(
        User.Name,
        db.func.sum(Wallet.Balance * MarketPrice.Price).label("Portfolio_Value")
    ).join(Wallet, User.UserID == Wallet.UserID)\
     .join(MarketPrice, Wallet.CryptoID == MarketPrice.CryptoID)\
     .group_by(User.UserID).all()

    return render_template('portfolio.html', portfolio_data=portfolio_data)

# -------------------------------
# 📊 Single User Dashboard
# -------------------------------
@bp.route('/user/<int:user_id>')
def user_dashboard(user_id):
    user = User.query.get(user_id)
    wallet = Wallet.query.filter_by(UserID=user_id).all()
    orders = Orders.query.filter_by(UserID=user_id).all()
    transactions = Transaction.query.filter_by(UserID=user_id).all()
    watchlist = Watchlist.query.filter_by(UserID=user_id).all()

    portfolio_value = db.session.query(
        db.func.sum(Wallet.Balance * MarketPrice.Price)
    ).join(MarketPrice, Wallet.CryptoID == MarketPrice.CryptoID)\
     .filter(Wallet.UserID == user_id).scalar() or 0

    return render_template(
        'dashboard.html',
        user=user,
        wallet=wallet,
        orders=orders,
        transactions=transactions,
        watchlist=watchlist,
        portfolio_value=portfolio_value
    )
