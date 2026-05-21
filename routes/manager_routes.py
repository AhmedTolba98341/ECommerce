# routes/manager_routes.py - Manager Routes

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from models import db, Order, Payment, Product, Customer, Review, OrderItem, Category
from sqlalchemy import func

manager_bp = Blueprint('manager', __name__)


def manager_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.Role not in ('Manager', 'Admin'):
            flash('Manager access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@manager_bp.route('/dashboard')
@login_required
@manager_required
def dashboard():
    total_orders    = Order.query.count()
    total_customers = Customer.query.count()
    total_revenue   = db.session.query(func.sum(Payment.Amount)).filter_by(Status='Verified').scalar() or 0
    pending_orders  = Order.query.filter_by(Status='Pending').count()

    # Monthly orders (last 6 months)
    monthly = db.session.query(
        func.month(Order.OrderDate).label('month'),
        func.count(Order.OrderID).label('count')
    ).group_by(func.month(Order.OrderDate)).limit(6).all()

    # Top products
    top_products = db.session.query(
        Product.ProductName,
        func.sum(OrderItem.Quantity).label('total_sold')
    ).join(OrderItem, Product.ProductID == OrderItem.ProductID)\
     .group_by(Product.ProductName)\
     .order_by(func.sum(OrderItem.Quantity).desc()).limit(5).all()

    return render_template('manager/dashboard.html',
        total_orders=total_orders,
        total_customers=total_customers,
        total_revenue=total_revenue,
        pending_orders=pending_orders,
        monthly=monthly,
        top_products=top_products
    )


@manager_bp.route('/reports')
@login_required
@manager_required
def reports():
    # Revenue by category
    rev_by_cat = db.session.query(
        Category.CategoryName,
        func.sum(OrderItem.UnitPrice * OrderItem.Quantity).label('revenue')
    ).join(Product, Category.CategoryID == Product.CategoryID)\
     .join(OrderItem, Product.ProductID == OrderItem.ProductID)\
     .group_by(Category.CategoryName).all()

    # Orders by status
    orders_by_status = db.session.query(
        Order.Status,
        func.count(Order.OrderID).label('count')
    ).group_by(Order.Status).all()

    total_sales = db.session.query(func.sum(Payment.Amount)).filter_by(Status='Verified').scalar() or 0

    return render_template('manager/reports.html',
        rev_by_cat=rev_by_cat,
        orders_by_status=orders_by_status,
        total_sales=total_sales
    )
