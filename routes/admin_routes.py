# routes/admin_routes.py - Admin Routes

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from models import db, User, Customer, Admin, Manager, Product, Category, Brand
from models import Order, OrderItem, Payment, Review, Discount, ProductDiscount, Report
from forms import ProductForm, CategoryForm, BrandForm, AddManagerForm, DiscountForm
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import func, text

bcrypt = Bcrypt()

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator: allow only Admin role."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.Role != 'Admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ── Dashboard ────────────────────────────────────────────────────────────────
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_products  = Product.query.count()
    total_customers = Customer.query.count()
    total_orders    = Order.query.count()
    pending_payments= Payment.query.filter_by(Status='Pending').count()
    pending_reviews = Review.query.filter_by(Status='Pending').count()
    recent_orders   = Order.query.order_by(Order.OrderDate.desc()).limit(5).all()

    # Revenue
    revenue = db.session.query(func.sum(Payment.Amount)).filter_by(Status='Verified').scalar() or 0

    return render_template('admin/dashboard.html',
        total_products=total_products, total_customers=total_customers,
        total_orders=total_orders, pending_payments=pending_payments,
        pending_reviews=pending_reviews, recent_orders=recent_orders,
        revenue=revenue)


# ── Products ─────────────────────────────────────────────────────────────────
@admin_bp.route('/products')
@login_required
@admin_required
def products():
    products = Product.query.order_by(Product.CreatedAt.desc()).all()
    return render_template('admin/products.html', products=products)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form = ProductForm()
    form.category_id.choices = [(c.CategoryID, c.CategoryName) for c in Category.query.all()]
    form.brand_id.choices    = [(b.BrandID,    b.BrandName)    for b in Brand.query.all()]

    if form.validate_on_submit():
        product = Product(
            ProductName=form.product_name.data,
            Description=form.description.data,
            Price=form.price.data,
            Stock=form.stock.data,
            ImageURL=form.image_url.data,
            CategoryID=form.category_id.data,
            BrandID=form.brand_id.data,
            IsActive=form.is_active.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, title='Add Product')


@admin_bp.route('/products/edit/<int:pid>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(pid):
    product = Product.query.get_or_404(pid)
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.CategoryID, c.CategoryName) for c in Category.query.all()]
    form.brand_id.choices    = [(b.BrandID,    b.BrandName)    for b in Brand.query.all()]

    if form.validate_on_submit():
        product.ProductName = form.product_name.data
        product.Description = form.description.data
        product.Price       = form.price.data
        product.Stock       = form.stock.data
        product.ImageURL    = form.image_url.data
        product.CategoryID  = form.category_id.data
        product.BrandID     = form.brand_id.data
        product.IsActive    = form.is_active.data
        db.session.commit()
        flash('Product updated.', 'success')
        return redirect(url_for('admin.products'))

    # Pre-fill
    form.product_name.data = product.ProductName
    form.category_id.data  = product.CategoryID
    form.brand_id.data     = product.BrandID
    return render_template('admin/product_form.html', form=form, title='Edit Product')


@admin_bp.route('/products/delete/<int:pid>', methods=['POST'])
@login_required
@admin_required
def delete_product(pid):
    product = Product.query.get_or_404(pid)
    product.IsActive = False   # Soft delete
    db.session.commit()
    flash('Product deactivated.', 'warning')
    return redirect(url_for('admin.products'))


# ── Categories ───────────────────────────────────────────────────────────────
@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    cats = Category.query.all()
    form = CategoryForm()
    return render_template('admin/categories.html', categories=cats, form=form)


@admin_bp.route('/categories/add', methods=['POST'])
@login_required
@admin_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        if Category.query.filter_by(CategoryName=form.category_name.data).first():
            flash('Category already exists.', 'danger')
        else:
            cat = Category(CategoryName=form.category_name.data, Description=form.description.data)
            db.session.add(cat)
            db.session.commit()
            flash('Category added.', 'success')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/categories/delete/<int:cid>', methods=['POST'])
@login_required
@admin_required
def delete_category(cid):
    cat = Category.query.get_or_404(cid)
    db.session.delete(cat)
    db.session.commit()
    flash('Category deleted.', 'warning')
    return redirect(url_for('admin.categories'))


# ── Brands ───────────────────────────────────────────────────────────────────
@admin_bp.route('/brands')
@login_required
@admin_required
def brands():
    brands = Brand.query.all()
    form   = BrandForm()
    return render_template('admin/brands.html', brands=brands, form=form)


@admin_bp.route('/brands/add', methods=['POST'])
@login_required
@admin_required
def add_brand():
    form = BrandForm()
    if form.validate_on_submit():
        if Brand.query.filter_by(BrandName=form.brand_name.data).first():
            flash('Brand already exists.', 'danger')
        else:
            brand = Brand(BrandName=form.brand_name.data, Country=form.country.data)
            db.session.add(brand)
            db.session.commit()
            flash('Brand added.', 'success')
    return redirect(url_for('admin.brands'))


@admin_bp.route('/brands/delete/<int:bid>', methods=['POST'])
@login_required
@admin_required
def delete_brand(bid):
    brand = Brand.query.get_or_404(bid)
    db.session.delete(brand)
    db.session.commit()
    flash('Brand deleted.', 'warning')
    return redirect(url_for('admin.brands'))


# ── Users ────────────────────────────────────────────────────────────────────
@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.CreatedAt.desc()).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/users/toggle/<int:uid>', methods=['POST'])
@login_required
@admin_required
def toggle_user(uid):
    user = User.query.get_or_404(uid)
    user.IsActive = not user.IsActive
    db.session.commit()
    status = 'activated' if user.IsActive else 'deactivated'
    flash(f'User {user.Username} {status}.', 'info')
    return redirect(url_for('admin.users'))


# ── Add Manager ───────────────────────────────────────────────────────────────
@admin_bp.route('/managers/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_manager():
    form = AddManagerForm()
    if form.validate_on_submit():
        if User.query.filter_by(Username=form.username.data).first():
            flash('Username taken.', 'danger')
        else:
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(Username=form.username.data, Email=form.email.data,
                        Password=hashed_pw, Role='Manager')
            db.session.add(user)
            db.session.flush()
            mgr = Manager(UserID=user.UserID, FullName=form.full_name.data)
            db.session.add(mgr)
            db.session.commit()
            flash('Manager account created.', 'success')
            return redirect(url_for('admin.users'))
    return render_template('admin/add_manager.html', form=form)


# ── Orders ───────────────────────────────────────────────────────────────────
@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    orders = Order.query.order_by(Order.OrderDate.desc()).all()
    return render_template('admin/orders.html', orders=orders)


@admin_bp.route('/orders/<int:oid>/status', methods=['POST'])
@login_required
@admin_required
def update_order_status(oid):
    order = Order.query.get_or_404(oid)
    order.Status = request.form.get('status', order.Status)
    db.session.commit()
    flash('Order status updated.', 'success')
    return redirect(url_for('admin.orders'))


# ── Payments ─────────────────────────────────────────────────────────────────
@admin_bp.route('/payments')
@login_required
@admin_required
def payments():
    payments = Payment.query.order_by(Payment.PaymentDate.desc()).all()
    return render_template('admin/payments.html', payments=payments)


@admin_bp.route('/payments/<int:pid>/verify', methods=['POST'])
@login_required
@admin_required
def verify_payment(pid):
    payment = Payment.query.get_or_404(pid)
    action  = request.form.get('action')
    if action == 'verify':
        payment.Status = 'Verified'
        flash('Payment verified.', 'success')
    elif action == 'reject':
        payment.Status = 'Rejected'
        flash('Payment rejected.', 'warning')
    db.session.commit()
    return redirect(url_for('admin.payments'))


# ── Reviews ──────────────────────────────────────────────────────────────────
@admin_bp.route('/reviews')
@login_required
@admin_required
def reviews():
    reviews = Review.query.order_by(Review.CreatedAt.desc()).all()
    return render_template('admin/reviews.html', reviews=reviews)


@admin_bp.route('/reviews/<int:rid>/moderate', methods=['POST'])
@login_required
@admin_required
def moderate_review(rid):
    review = Review.query.get_or_404(rid)
    action = request.form.get('action')
    if action == 'approve':
        review.Status = 'Approved'
        flash('Review approved.', 'success')
    elif action == 'reject':
        review.Status = 'Rejected'
        flash('Review rejected.', 'warning')
    db.session.commit()
    return redirect(url_for('admin.reviews'))


# ── Discounts ─────────────────────────────────────────────────────────────────
@admin_bp.route('/discounts')
@login_required
@admin_required
def discounts():
    discounts = Discount.query.all()
    form      = DiscountForm()
    products  = Product.query.filter_by(IsActive=True).all()
    return render_template('admin/discounts.html', discounts=discounts, form=form, products=products)


@admin_bp.route('/discounts/add', methods=['POST'])
@login_required
@admin_required
def add_discount():
    form = DiscountForm()
    if form.validate_on_submit():
        d = Discount(
            DiscountName=form.discount_name.data,
            DiscountPercent=form.discount_percent.data,
            IsActive=form.is_active.data
        )
        db.session.add(d)
        db.session.commit()
        flash('Discount added.', 'success')
    return redirect(url_for('admin.discounts'))


# ── Reports ───────────────────────────────────────────────────────────────────
@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    # Total sales
    total_sales = db.session.query(func.sum(Payment.Amount)).filter_by(Status='Verified').scalar() or 0

    # Most sold products
    top_products = db.session.query(
        Product.ProductName,
        func.sum(OrderItem.Quantity).label('total_sold')
    ).join(OrderItem, Product.ProductID == OrderItem.ProductID)\
     .group_by(Product.ProductName)\
     .order_by(func.sum(OrderItem.Quantity).desc()).limit(5).all()

    # Revenue by category
    rev_by_cat = db.session.query(
        Category.CategoryName,
        func.sum(OrderItem.UnitPrice * OrderItem.Quantity).label('revenue')
    ).join(Product, Category.CategoryID == Product.CategoryID)\
     .join(OrderItem, Product.ProductID == OrderItem.ProductID)\
     .group_by(Category.CategoryName).all()

    # Pending payments
    pending_payments = Payment.query.filter_by(Status='Pending').count()

    # Total customers
    total_customers = Customer.query.count()

    # Orders per status
    orders_by_status = db.session.query(
        Order.Status,
        func.count(Order.OrderID).label('count')
    ).group_by(Order.Status).all()

    # Top rated products
    top_rated = db.session.query(
        Product.ProductName,
        func.avg(Review.Rating).label('avg_rating'),
        func.count(Review.ReviewID).label('review_count')
    ).join(Review, Product.ProductID == Review.ProductID)\
     .filter(Review.Status == 'Approved')\
     .group_by(Product.ProductName)\
     .order_by(func.avg(Review.Rating).desc()).limit(5).all()

    return render_template('admin/reports.html',
        total_sales=total_sales,
        top_products=top_products,
        rev_by_cat=rev_by_cat,
        pending_payments=pending_payments,
        total_customers=total_customers,
        orders_by_status=orders_by_status,
        top_rated=top_rated
    )
