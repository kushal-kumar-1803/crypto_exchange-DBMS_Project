from flask import Flask, redirect, url_for
from extensions import db, login_manager
from flask_login import current_user
import pymysql

# Import blueprints
from routes.public_routes import bp as public_bp
from routes.admin_routes import bp as admin_bp
from routes.user_routes import bp as user_bp


# ======================================================
# ✅ APP FACTORY FUNCTION
# ======================================================
def create_app():
    app = Flask(__name__)

    # --------------------------
    # ⚙️ CONFIGURATION
    # --------------------------
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass123@localhost/crypto_exchange'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'supersecretkey'  # 🔐 safer key for production

    # --------------------------
    # 🔗 INITIALIZE EXTENSIONS
    # --------------------------
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    # --------------------------
    # 👤 LOGIN MANAGER SETUP
    # --------------------------
    from models.user_models import User
    from models.admin_models import AdminUser

    @login_manager.user_loader
    def load_user(user_id):
        """
        Distinguish between admin and normal users.
        Admin IDs are stored as 'admin-<id>' in sessions.
        """
        if str(user_id).startswith("admin-"):
            admin_id = user_id.split("-")[1]
            return AdminUser.query.get(int(admin_id))
        return User.query.get(int(user_id))

    # --------------------------
    # 🌐 REGISTER BLUEPRINTS
    # --------------------------
    app.register_blueprint(public_bp)  # Public routes
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # --------------------------
    # 🧠 CONTEXT PROCESSOR
    # --------------------------
    @app.context_processor
    def inject_user():
        """Make `current_user` available globally in templates"""
        return dict(current_user=current_user)

    # --------------------------
    # 🏠 REDIRECT ROOT TO LOGIN
    # --------------------------
    @app.route('/')
    def home_redirect():
        return redirect(url_for('user.login'))

    # --------------------------
    # 🧪 CONNECTION TEST ROUTE
    # --------------------------
    @app.route('/ping')
    def ping():
        return "✅ Flask app connected to MySQL successfully!"

    # --------------------------
    # 🗃️ DATABASE INITIALIZATION
    # --------------------------
    with app.app_context():
        from models.admin_models import AdminUser
        from models.user_models import User, Wallet
        from models.crypto_models import Watchlist
        from models.crypto_models import Cryptocurrency, MarketPrice, Orders, Transaction

        db.create_all()

        # ✅ Ensure a default admin exists
        admin_exists = AdminUser.query.filter_by(Username='admin@gmail.com').first()
        if not admin_exists:
            default_admin = AdminUser(Username='admin@gmail.com', Password='admin123')
            db.session.add(default_admin)
            db.session.commit()
            print("👑 Default admin created: admin@gmail.com / admin123")

        print("✅ Database tables verified and initialized.")

    return app


# ======================================================
# 🚀 MAIN ENTRY POINT
# ======================================================
if __name__ == '__main__':
    pymysql.install_as_MySQLdb()
    app = create_app()
    print("🚀 Crypto Exchange App running at: http://127.0.0.1:5000")
    app.run(debug=True)
