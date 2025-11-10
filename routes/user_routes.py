from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from models.user_models import User, Wallet
from models.crypto_models import Watchlist
from models.admin_models import AdminUser
from sqlalchemy import func
from models.crypto_models import Cryptocurrency, Orders, MarketPrice, Transaction
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from decimal import Decimal
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('user', __name__, url_prefix='/user')

# ======================================================
# 🔐 LOGIN PAGE
# ======================================================
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(Email=email).first()

        if user and check_password_hash(user.Password, password):
            login_user(user)
            flash('✅ Login successful!', 'success')
            return redirect(url_for('user.dashboard'))
        else:
            flash('❌ Invalid email or password.', 'danger')

    return render_template('user/user_login.html')


# ======================================================
# 📊 DASHBOARD — show all cryptos + latest price
# ======================================================
@bp.route('/dashboard')
@login_required
def dashboard():
    cryptos = Cryptocurrency.query.all()

    # Get latest MarketPrice for each crypto
    subq = (
        db.session.query(
            MarketPrice.CryptoID,
            func.max(MarketPrice.DateTime).label("max_dt")
        ).group_by(MarketPrice.CryptoID).subquery()
    )

    latest_prices = (
        db.session.query(MarketPrice)
        .join(subq, (MarketPrice.CryptoID == subq.c.CryptoID) & (MarketPrice.DateTime == subq.c.max_dt))
        .all()
    )
    price_map = {mp.CryptoID: mp for mp in latest_prices}

    # Attach latest price
    for c in cryptos:
        c.market_price = price_map.get(c.CryptoID)

    return render_template('user/dashboard.html', user=current_user, cryptos=cryptos)

# ======================================================
# 💼 WALLET
# ======================================================
@bp.route('/wallet')
@login_required
def wallet():
    wallet_data = (
        db.session.query(Wallet, Cryptocurrency)
        .join(Cryptocurrency, Wallet.CryptoID == Cryptocurrency.CryptoID)
        .filter(Wallet.UserID == current_user.UserID)
        .all()
    )

    total_value = db.session.query(
        db.func.sum(Wallet.Balance * MarketPrice.Price)
    ).join(MarketPrice, Wallet.CryptoID == MarketPrice.CryptoID)\
     .filter(Wallet.UserID == current_user.UserID).scalar() or 0

    return render_template('user/wallet.html', user=current_user, wallet_data=wallet_data, total_value=total_value)


# ======================================================
# 💳 TRANSACTIONS
# ======================================================
@bp.route('/transactions')
@login_required
def transactions_page():
    transactions = (
        db.session.query(Transaction, Orders, Cryptocurrency)
        .join(Orders, Transaction.OrderID == Orders.OrderID)
        .join(Cryptocurrency, Orders.CryptoID == Cryptocurrency.CryptoID)
        .filter(Transaction.UserID == current_user.UserID)
        .order_by(Transaction.Timestamp.desc())
        .all()
    )
    return render_template('user/transactions.html', user=current_user, transactions=transactions)

# ======================================================
# ⭐ WATCHLIST
# ======================================================
@bp.route('/watchlist')
@login_required
def watchlist():
    watchlist_data = (
        db.session.query(Watchlist, Cryptocurrency)
        .join(Cryptocurrency, Watchlist.CryptoID == Cryptocurrency.CryptoID)
        .filter(Watchlist.UserID == current_user.UserID)
        .all()
    )
    return render_template('user/watchlist.html', user=current_user, watchlist_data=watchlist_data)


# ✅ Add crypto to watchlist
@bp.route('/add_to_watchlist/<int:crypto_id>', methods=['POST'])
@login_required
def add_to_watchlist(crypto_id):
    existing = Watchlist.query.filter_by(UserID=current_user.UserID, CryptoID=crypto_id).first()
    if existing:
        flash('⚠️ Already in your watchlist.', 'info')
    else:
        new_entry = Watchlist(UserID=current_user.UserID, CryptoID=crypto_id)
        db.session.add(new_entry)
        db.session.commit()
        flash('⭐ Added to watchlist successfully!', 'success')
    return redirect(url_for('user.dashboard'))


# ✅ Remove crypto from watchlist
@bp.route('/remove_from_watchlist/<int:crypto_id>', methods=['POST'])
@login_required
def remove_from_watchlist(crypto_id):
    entry = Watchlist.query.filter_by(UserID=current_user.UserID, CryptoID=crypto_id).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()
        flash('🗑️ Removed from watchlist.', 'success')
    else:
        flash('⚠️ Item not found in your watchlist.', 'warning')
    return redirect(url_for('user.watchlist'))

# ======================================================
# 🏠 PROFILE
# ======================================================
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    if request.method == 'POST':
        user.Name = request.form.get('name')
        user.Phone = request.form.get('phone')
        db.session.commit()
        flash('✅ Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))

    return render_template('user/profile.html', user=user)


# ======================================================
# 💸 BUY CRYPTO
# ======================================================
@bp.route('/buy/<int:crypto_id>', methods=['POST'])
@login_required
def buy_crypto(crypto_id):
    crypto = Cryptocurrency.query.get_or_404(crypto_id)
    quantity = Decimal(request.form.get('quantity', '0'))

    # Fetch latest price
    latest_price_entry = (
        MarketPrice.query.filter_by(CryptoID=crypto.CryptoID)
        .order_by(MarketPrice.DateTime.desc())
        .first()
    )
    price = Decimal(str(latest_price_entry.Price)) if latest_price_entry else Decimal('100.00')

    # Create order
    order = Orders(
        UserID=current_user.UserID,
        CryptoID=crypto.CryptoID,
        OrderType='BUY',
        Quantity=quantity,
        Price=price,
        Status='Completed',
        Timestamp=datetime.utcnow()
    )
    db.session.add(order)
    db.session.flush()

    # Create transaction
    transaction = Transaction(
        OrderID=order.OrderID,
        UserID=current_user.UserID,
        Amount=quantity * price,
        TransactionType='BUY',
        Timestamp=datetime.utcnow()
    )
    db.session.add(transaction)

    # Update wallet
    wallet = Wallet.query.filter_by(UserID=current_user.UserID, CryptoID=crypto.CryptoID).first()
    if wallet:
        wallet.Balance += quantity
    else:
        wallet = Wallet(UserID=current_user.UserID, CryptoID=crypto.CryptoID, Balance=quantity)
        db.session.add(wallet)

    db.session.commit()
    flash(f'✅ Bought {quantity} units of {crypto.Name} at ${price} each!', 'success')
    return redirect(url_for('user.transactions_page'))


# ======================================================
# 💰 SELL CRYPTO
# ======================================================
@bp.route('/sell/<int:crypto_id>', methods=['POST'])
@login_required
def sell_crypto(crypto_id):
    crypto = Cryptocurrency.query.get_or_404(crypto_id)
    quantity = Decimal(request.form.get('quantity', '0'))

    # Fetch latest price
    latest_price_entry = (
        MarketPrice.query.filter_by(CryptoID=crypto.CryptoID)
        .order_by(MarketPrice.DateTime.desc())
        .first()
    )
    price = Decimal(str(latest_price_entry.Price)) if latest_price_entry else Decimal('100.00')

    wallet = Wallet.query.filter_by(UserID=current_user.UserID, CryptoID=crypto.CryptoID).first()
    if not wallet or wallet.Balance < quantity:
        flash(f'⚠️ Not enough {crypto.Symbol} balance to sell!', 'warning')
        return redirect(url_for('user.dashboard'))

    # Create order
    order = Orders(
        UserID=current_user.UserID,
        CryptoID=crypto.CryptoID,
        OrderType='SELL',
        Quantity=quantity,
        Price=price,
        Status='Completed',
        Timestamp=datetime.utcnow()
    )
    db.session.add(order)
    db.session.flush()

    # Create transaction
    transaction = Transaction(
        OrderID=order.OrderID,
        UserID=current_user.UserID,
        Amount=quantity * price,
        TransactionType='SELL',
        Timestamp=datetime.utcnow()
    )
    db.session.add(transaction)

    wallet.Balance -= quantity
    db.session.commit()

    flash(f'💰 Sold {quantity} units of {crypto.Name} at ${price} each!', 'success')
    return redirect(url_for('user.transactions_page'))

# ======================================================
# 📊 PORTFOLIO
# ======================================================
@bp.route('/portfolio')
@login_required
def portfolio():
    # join Wallet → Cryptocurrency → MarketPrice
    portfolio_data = (
        db.session.query(Wallet, Cryptocurrency, MarketPrice)
        .join(Cryptocurrency, Wallet.CryptoID == Cryptocurrency.CryptoID)
        .join(MarketPrice, Wallet.CryptoID == MarketPrice.CryptoID)
        .filter(Wallet.UserID == current_user.UserID)
        .all()
    )

    total_value = 0
    portfolio_summary = []

    for wallet, crypto, price in portfolio_data:
        value = float(wallet.Balance) * float(price.Price)
        total_value += value
        portfolio_summary.append({
            "crypto": crypto.Name,
            "symbol": crypto.Symbol,
            "balance": float(wallet.Balance),
            "price": float(price.Price),
            "value": round(value, 2)
        })

    return render_template(
        'user/portfolio.html',
        user=current_user,
        portfolio=portfolio_summary,
        total_value=round(total_value, 2)
    )


# ======================================================
# 🚪 LOGOUT
# ======================================================
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have logged out successfully.', 'info')
    return redirect(url_for('user.login'))
