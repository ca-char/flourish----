from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_limiter import Limiter
from web_app.models import User
from web_app.extensions import db, bcrypt
from web_app.forms import LoginForm, RegisterForm, LogoutForm
from web_app.extensions import limiter
import logging

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
@limiter.limit("20 per hour")
def login():
    """
    Processes a login form submission, checks if the user inputted email and
      password are in the DB and logs the user in if credentials are valid.
    """
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            logging.warning("Successful login for user_id={user.user_id} from IP: {request.remote_addr}")
            return redirect(url_for('views.admin_base' if user.is_admin else 'views.user_base'))
        flash('Invalid email or incorrect password. Please try again.', category='error')
    else:
        if request.method == 'POST':
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='error')

    return render_template("login.html", user=current_user, form=form)

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        flash('Logged out successfully.', category='success')
        return redirect(url_for('auth.login'))
    else:
        flash('Invalid logout attempt (CSRF token missing or invalid).', category='error')
        return redirect(url_for('views.user_base'))

# @auth.route('/register', methods=['GET', 'POST'])
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        password1 = form.password1.data

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=bcrypt.generate_password_hash(password1).decode('utf-8')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.user_base'))
    
    elif request.method == 'POST':
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, category='error')

    return render_template("register.html", user=current_user, form=form)