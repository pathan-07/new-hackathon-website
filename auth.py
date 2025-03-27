
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
import random
from app import db, mail
from models import User
from forms import LoginForm, SignupForm, OTPForm

auth = Blueprint('auth', __name__)

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp_email(email, otp):
    try:
        msg = Message('Your OTP for Verification',
                    sender=os.environ.get('MAIL_USERNAME'),
                    recipients=[email])
        msg.body = f'Your OTP is: {otp}\nThis code will expire in 10 minutes.'
        msg.html = f'''
            <h3>Your OTP Verification Code</h3>
            <p>Your OTP is: <strong>{otp}</strong></p>
            <p>This code will expire in 10 minutes.</p>
        '''
        mail.send(msg)
        # Store OTP with timestamp
        session['login_otp'] = otp
        session['otp_timestamp'] = datetime.utcnow().timestamp()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        # Generate and send OTP
        otp = generate_otp()
        session['login_otp'] = otp
        session['user_email'] = email
        
        if send_otp_email(email, otp):
            return redirect(url_for('auth.verify_otp'))
        else:
            flash('Error sending OTP. Please try again.')
            return redirect(url_for('auth.login'))

    return render_template('login.html', form=form)

@auth.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    form = OTPForm()
    if form.validate_on_submit():
        entered_otp = form.otp.data
        stored_otp = session.get('login_otp')
        user_email = session.get('user_email')

        if not stored_otp or not user_email:
            flash('Session expired. Please login again.')
            return redirect(url_for('auth.login'))

        # Check if OTP is expired (10 minutes)
        otp_timestamp = session.get('otp_timestamp')
        if not otp_timestamp or (datetime.utcnow().timestamp() - otp_timestamp) > 600:
            flash('OTP has expired. Please request a new one.')
            return redirect(url_for('auth.login'))

        if entered_otp == stored_otp:
            user = User.query.filter_by(email=user_email).first()
            login_user(user)
            # Clear session data
            session.pop('login_otp', None)
            session.pop('user_email', None)
            session.pop('otp_timestamp', None)
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid OTP. Please try again.')

    return render_template('verify_otp.html', form=form, email=session.get('user_email'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        password = form.password.data

        if User.query.filter_by(email=email).first():
            flash('Email already exists.')
            return redirect(url_for('auth.signup'))

        new_user = User(
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
