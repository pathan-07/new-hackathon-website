import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from flask_mail import Mail
from datetime import datetime, timedelta
from flask_migrate import Migrate

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
mail = Mail()
# Create the app
app = Flask(__name__)
# Generate a random secret key for each session if not set in environment
app.secret_key = os.environ.get("SESSION_SECRET") or os.urandom(24)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or os.urandom(24)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///app.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Configure mail settings
app.config['MAIL_SERVER'] = 'pathanfaizan0712@gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# Initialize extensions
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

# Configure login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Import routes after app creation to avoid circular imports
from models import User, Scholarship
from auth import auth as auth_blueprint
from google_auth import google_auth as google_auth_blueprint
from routes import routes as routes_blueprint
from chatbot import chatbot as chatbot_blueprint

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(google_auth_blueprint)
app.register_blueprint(routes_blueprint)
app.register_blueprint(chatbot_blueprint)

# Create database tables and add sample data
with app.app_context():
    try:
        db.create_all()
        
        # Add a default admin user if none exists
        if User.query.filter_by(email='admin@example.com').first() is None:
            admin_user = User(email='admin@example.com')
            admin_user.set_password('adminpassword')
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created")
        
        # Add sample scholarships if none exist
        if Scholarship.query.count() == 0:
            sample_scholarships = [
                Scholarship(
                    title="STEM Excellence Scholarship",
                    description="For outstanding students pursuing degrees in Science, Technology, Engineering, or Mathematics.",
                    deadline=datetime.utcnow() + timedelta(days=30),
                    amount="$5,000",
                    eligibility="Undergraduate STEM students with GPA 3.5+"
                ),
                Scholarship(
                    title="Future Leaders Grant",
                    description="Supporting students who demonstrate exceptional leadership qualities in their communities.",
                    deadline=datetime.utcnow() + timedelta(days=60),
                    amount="$3,000",
                    eligibility="All undergraduate students with leadership experience"
                ),
                Scholarship(
                    title="Global Diversity Scholarship",
                    description="Promoting diversity and inclusion in higher education.",
                    deadline=datetime.utcnow() + timedelta(days=45),
                    amount="$4,000",
                    eligibility="All students promoting diversity initiatives"
                )
            ]

            for scholarship in sample_scholarships:
                db.session.add(scholarship)

            db.session.commit()
            print("Sample scholarships added successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
