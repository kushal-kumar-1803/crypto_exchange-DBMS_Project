from flask import Flask
from extensions import db, login_manager
from flask_login import current_user
import pymysql

# Import blueprints (modular routes)
from routes.public_routes import bp as public_bp
from routes.admin_routes import bp as admin_bp


# ======================================================
# ✅ App Factory Function
# ======================================================
def create_app():
    app = Flask(__name__)

    # --------------------------
    # 🧩 Basic Configurations
    # --------------------------
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass123@localhost/crypto_exchange'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'admin'  # Used for sessions and flash messages

    # --------------------------
    # 🔗 Initialize Extensions
    # --------------------------
    db.init_app(app)
    login_manager.init_app(app)

    # --------------------------
    # 🧩 User Loader for Flask-Login
    # --------------------------
    from models import User
    from models.admin_models import AdminUser

    @login_manager.user_loader
    def load_user(user_id):
        # Try loading admin first
        admin = AdminUser.query.get(int(user_id))
        if admin:
            return admin

        # Otherwise, load normal user
        return User.query.get(int(user_id))

    # --------------------------
    # 🌐 Register Blueprints
    # --------------------------
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # --------------------------
    # ✅ Context processor for templates
    # --------------------------
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    # --------------------------
    # 🏠 Root route check
    # --------------------------
    @app.route('/ping')
    def ping():
        return "✅ Flask app connected to MySQL successfully!"

    return app


# ======================================================
# 🚀 Run App
# ======================================================
if __name__ == '__main__':
    pymysql.install_as_MySQLdb()  # ensure PyMySQL works like MySQLdb
    app = create_app()

    print("✅ Crypto Exchange App Running at: http://127.0.0.1:5000")
    app.run(debug=True)
