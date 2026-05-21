# routes/auth_routes.py - Authentication Routes

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Customer, Admin, Manager
from forms import LoginForm, RegisterForm

bcrypt = Bcrypt()

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return _redirect_by_role(current_user.Role)

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Username=form.username.data).first()
        if user and user.IsActive and bcrypt.check_password_hash(user.Password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome back, {user.Username}!', 'success')
            return _redirect_by_role(user.Role)
        flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        # Check uniqueness
        if User.query.filter_by(Username=form.username.data).first():
            flash('Username already taken.', 'danger')
            return render_template('register.html', form=form)
        if User.query.filter_by(Email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html', form=form)

        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            Username=form.username.data,
            Email=form.email.data,
            Password=hashed_pw,
            Role='Customer'
        )
        db.session.add(user)
        db.session.flush()   # get UserID

        customer = Customer(
            UserID=user.UserID,
            FullName=form.full_name.data,
            Phone=form.phone.data,
            Address=form.address.data
        )
        db.session.add(customer)
        db.session.flush()

        # Create empty cart for customer
        from models import ShoppingCart
        cart = ShoppingCart(CustomerID=customer.CustomerID)
        db.session.add(cart)

        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


def _redirect_by_role(role):
    if role == 'Admin':
        return redirect(url_for('admin.dashboard'))
    elif role == 'Manager':
        return redirect(url_for('manager.dashboard'))
    else:
        return redirect(url_for('customer.dashboard'))
