from extensions import db
from datetime import datetime
from flask_login import UserMixin


# =====================================================
# 👤 USER MODEL
# =====================================================
class User(UserMixin, db.Model):
    __tablename__ = 'User'
    __table_args__ = {'extend_existing': True}

    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    wallets = db.relationship('Wallet', back_populates='user', lazy=True)
    orders = db.relationship('Orders', backref='user', lazy=True)
    portfolios = db.relationship('Portfolio', backref='user', lazy=True)
    transactions = db.relationship('Transaction', back_populates='user', lazy=True)

    # ✅ This is the fix — Flask-Login needs to know your primary key
    def get_id(self):
        return str(self.UserID)

    def __repr__(self):
        return f"<User {self.Name} ({self.Email})>"


# =====================================================
# 💰 WALLET MODEL
# =====================================================
class Wallet(db.Model):
    __tablename__ = 'Wallet'
    __table_args__ = {'extend_existing': True}

    # Composite primary key
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), primary_key=True)
    CryptoID = db.Column(db.Integer, db.ForeignKey('Cryptocurrency.CryptoID'), primary_key=True)
    Balance = db.Column(db.Numeric(18, 8), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='wallets')
    crypto = db.relationship('Cryptocurrency', back_populates='wallets')

    def __repr__(self):
        return f"<Wallet User={self.UserID}, Crypto={self.CryptoID}, Balance={self.Balance}>"   