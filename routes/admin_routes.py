# routes/admin_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db

# Import models directly from their modules (avoid generic `from models import ...`)
from models.admin_models import AdminUser
from models.user_models import User
from models.crypto_models import Cryptocurrency

# Optional: Orders / Portfolio may be in crypto_models (adjust names if your file uses different class names)
# If your file has class name `Orders`, we import it as Orders. If it is `Order`, change accordingly.
try:
    from models.crypto_models import Orders as OrderModel
except Exception:
    OrderModel = None

try:
    from models.crypto_models import Portfolio as PortfolioModel
except Exception:
    PortfolioModel = None

# Password helpers
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('admin', __name__, url_prefix='/admin')


# ======================================================
# Admin required decorator (session-based)
# ======================================================
def admin_required(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('admin_id'):
            flash('Please log in as admin first.', 'warning')
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)

    return wrapper


# ======================================================
# Admin Login
# ======================================================
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in as admin (session), go to dashboard
    if session.get('admin_id'):
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the admin by username
        admin = AdminUser.query.filter_by(Username=username).first()

        if admin:
            # check_password_hash expects the stored password to be hashed
            if check_password_hash(admin.Password, password):
                session['admin_id'] = admin.AdminID
                flash('✅ Admin logged in successfully!', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('❌ Incorrect password.', 'danger')
        else:
            flash('❌ No admin found with that username.', 'danger')

    return render_template('admin/admin_login.html')


# ======================================================
# Admin Logout
# ======================================================
@bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    flash('Admin logged out successfully.', 'info')
    return redirect(url_for('public.index'))


# ======================================================
# Admin Dashboard - shows users, cryptos, orders, portfolios
# ======================================================
@bp.route('/dashboard')
@admin_required
def dashboard():
    # Fetch users and cryptos
    users = User.query.all()
    cryptos = Cryptocurrency.query.all()

    # Load recent orders if OrderModel is available
    orders = []
    if OrderModel is not None:
        # adjust ordering/fields to match your model
        try:
            orders = OrderModel.query.order_by(OrderModel.OrderID.desc()).limit(20).all()
        except Exception:
            # fallback: try using a different column name
            try:
                orders = OrderModel.query.order_by(OrderModel.OrderDate.desc()).limit(20).all()
            except Exception:
                orders = []

    # Attach portfolio items to each user (if PortfolioModel exists)
    if PortfolioModel is not None:
        for u in users:
            try:
                u.portfolio = PortfolioModel.query.filter_by(UserID=u.UserID).all()
            except Exception:
                u.portfolio = []
    else:
        # ensure attribute exists for template
        for u in users:
            u.portfolio = []

    return render_template(
        'admin/dashboard.html',
        users=users,
        cryptos=cryptos,
        orders=orders
    )


# ======================================================
# Manage Users view
# ======================================================
@bp.route('/users')
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)


# ======================================================
# Add cryptocurrency
# ======================================================
@bp.route('/add_crypto', methods=['GET', 'POST'])
@admin_required
def add_crypto():
    if request.method == 'POST':
        name = request.form.get('name')
        symbol = request.form.get('symbol')
        blockchain = request.form.get('blockchain')
        launch_date = request.form.get('launch_date') or None

        crypto = Cryptocurrency(
            Name=name,
            Symbol=symbol,
            BlockchainType=blockchain,
            LaunchDate=launch_date
        )
        db.session.add(crypto)
        db.session.commit()
        flash('✅ New cryptocurrency added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/add_crypto.html')


# ======================================================
# Create admin (one-time)
# ======================================================
@bp.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if AdminUser.query.filter_by(Username=username).first():
            flash('❌ Username already exists.', 'danger')
            return redirect(url_for('admin.create_admin'))

        hashed = generate_password_hash(password)
        new_admin = AdminUser(Username=username, Password=hashed)
        db.session.add(new_admin)
        db.session.commit()

        flash('✅ New admin created successfully!', 'success')
        return redirect(url_for('admin.login'))

    return render_template('admin/create_admin.html')
