from extensions import db
from datetime import datetime


# =====================================================
# 🌐 CRYPTOCURRENCY MODEL
# =====================================================
class Cryptocurrency(db.Model):
    __tablename__ = 'Cryptocurrency'
    __table_args__ = {'extend_existing': True}

    CryptoID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Symbol = db.Column(db.String(10), nullable=False)
    BlockchainType = db.Column(db.String(30))
    LaunchDate = db.Column(db.Date)

    # ✅ Relationships
    market_prices = db.relationship('MarketPrice', backref='crypto', lazy=True)
    orders = db.relationship('Orders', backref='crypto', lazy=True)
    portfolios = db.relationship('Portfolio', backref='crypto', lazy=True)
    watchlists = db.relationship('Watchlist', backref='crypto', lazy=True)
    wallets = db.relationship('Wallet', back_populates='crypto', lazy=True)


    def __repr__(self):
        return f"<Crypto {self.Symbol}>"


# =====================================================
# 💹 MARKET PRICE MODEL
# =====================================================
class MarketPrice(db.Model):
    __tablename__ = 'MarketPrice'
    __table_args__ = {'extend_existing': True}

    PriceID = db.Column(db.Integer, primary_key=True)
    CryptoID = db.Column(db.Integer, db.ForeignKey('Cryptocurrency.CryptoID'))
    DateTime = db.Column(db.DateTime, default=datetime.utcnow)
    Price = db.Column(db.Numeric(15, 2))

    def __repr__(self):
        return f"<MarketPrice CryptoID={self.CryptoID}, Price={self.Price}>"


# =====================================================
# 🛒 ORDERS MODEL
# =====================================================
class Orders(db.Model):
    __tablename__ = 'Orders'
    __table_args__ = {'extend_existing': True}

    OrderID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    CryptoID = db.Column(db.Integer, db.ForeignKey('Cryptocurrency.CryptoID'))
    OrderType = db.Column(db.String(10))  # BUY / SELL
    Quantity = db.Column(db.Numeric(10, 2))
    Price = db.Column(db.Numeric(15, 2))
    Status = db.Column(db.String(20))
    Timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Order {self.OrderType} {self.CryptoID} by User {self.UserID}>"


# =====================================================
# 💸 TRANSACTION MODEL
# =====================================================
class Transaction(db.Model):
    __tablename__ = 'Transactions'
    __table_args__ = {'extend_existing': True}

    TransactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('Orders.OrderID', ondelete='CASCADE'))
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID', ondelete='CASCADE'))
    Amount = db.Column(db.Numeric(15, 2))
    TransactionType = db.Column(db.String(20))  # DEBIT / CREDIT
    Timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ Keep only one-side relationship (no duplicate 'user' backref)
    order = db.relationship('Orders', backref='transactions', lazy=True)
    user = db.relationship('User', back_populates='transactions')

    def __repr__(self):
        return f"<Transaction {self.TransactionType} - {self.Amount}>"


# =====================================================
# ⭐ WATCHLIST MODEL
# =====================================================
class Watchlist(db.Model):
    __tablename__ = 'Watchlist'
    __table_args__ = {'extend_existing': True}

    WatchlistID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    CryptoID = db.Column(db.Integer, db.ForeignKey('Cryptocurrency.CryptoID'))
    DateAdded = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Watchlist User={self.UserID}, Crypto={self.CryptoID}>"


# =====================================================
# 📊 PORTFOLIO MODEL
# =====================================================
class Portfolio(db.Model):
    __tablename__ = 'Portfolio'
    __table_args__ = {'extend_existing': True}

    PortfolioID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    CryptoID = db.Column(db.Integer, db.ForeignKey('Cryptocurrency.CryptoID'))
    Quantity = db.Column(db.Float)

    def __repr__(self):
        return f"<Portfolio User={self.UserID}, Crypto={self.CryptoID}, Qty={self.Quantity}>"
