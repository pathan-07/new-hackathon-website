from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Scholarship

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('routes.dashboard'))
        return render_template('index.html')
    except Exception as e:
        print(f"Error in index route: {e}")
        return "An error occurred. Please try again.", 500

@routes.route('/dashboard')
@login_required
def dashboard():
    # Get all scholarships from the database
    scholarships = Scholarship.query.order_by(Scholarship.created_at.desc()).all()
    return render_template('dashboard.html', scholarships=scholarships)