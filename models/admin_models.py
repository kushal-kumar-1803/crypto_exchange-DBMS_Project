from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class AdminUser(UserMixin, db.Model):
    __tablename__ = 'AdminUser'  # 👈 Make sure this matches the actual table name in MySQL
    __table_args__ = {'extend_existing': True}

    AdminID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)

    # ✅ Utility method to hash a new password
    def set_password(self, password):
        self.Password = generate_password_hash(password)

    # ✅ Check a password against the hashed value
    def check_password(self, password):
        return check_password_hash(self.Password, password)

    # ✅ Required by Flask-Login
    def get_id(self):
        return str(self.AdminID)

    def __repr__(self):
        return f"<AdminUser {self.Username}>"
