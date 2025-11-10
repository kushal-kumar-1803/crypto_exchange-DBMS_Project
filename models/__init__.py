from extensions import db

# ✅ Import models explicitly (avoid circular imports)
from models.user_models import User, Wallet
from models.crypto_models import Watchlist
from models.crypto_models import Cryptocurrency, MarketPrice, Orders, Transaction
from models.admin_models import AdminUser

__all__ = [
    "User",
    "Wallet",
    "Cryptocurrency",
    "MarketPrice",
    "Orders",
    "Transaction",
    "AdminUser",
]
