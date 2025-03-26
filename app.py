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
                    title="National Scholarship Portal (NSP)",
                    description="A central government scholarship scheme for students from minority communities and economically weaker sections. Covers pre-matric, post-matric, and merit-cum-means based scholarship programs.",
                    deadline=datetime.utcnow() + timedelta(days=90),
                    amount="₹5,000 - ₹100,000 per annum",
                    eligibility="Family income less than ₹2.5 lakhs per annum, minimum 50% marks in previous examination"
                ),
                Scholarship(
                    title="AICTE Pragati Scholarship",
                    description="Scholarship scheme by AICTE for girl students in technical education. Aims to promote technical education among females and provide financial support.",
                    deadline=datetime.utcnow() + timedelta(days=60),
                    amount="₹50,000 per annum",
                    eligibility="Girl students admitted to AICTE approved institutions, family income less than ₹8 lakhs per annum"
                ),
                Scholarship(
                    title="Prime Minister's Scholarship Scheme",
                    description="Special scholarship for Central Armed Police Forces and State Police Personnel wards. Supports professional and technical programs at graduate level.",
                    deadline=datetime.utcnow() + timedelta(days=45),
                    amount="₹36,000 per annum",
                    eligibility="Wards of serving/retired CAPF & Assam Rifles personnel"
                ),
                Scholarship(
                    title="Kishore Vaigyanik Protsahan Yojana (KVPY)",
                    description="Fellowship program to encourage students to pursue research careers in basic sciences. Provides monthly stipend and annual contingency grant.",
                    deadline=datetime.utcnow() + timedelta(days=75),
                    amount="₹5,000 - ₹7,000 monthly",
                    eligibility="Students in Class 11, 12 and First Year BSc/Integrated MSc, minimum 75% marks"
                )
            ]

            for scholarship in sample_scholarships:
                db.session.add(scholarship)

            db.session.commit()
            print("Sample scholarships added successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
