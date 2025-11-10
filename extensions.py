from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()

# Default login view for unauthorized users
login_manager.login_view = 'admin.login'  
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"
