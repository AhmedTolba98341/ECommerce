# routes/customer_routes.py - Customer Routes

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from models import db, Customer, Product, ShoppingCart, CartItem, Order, OrderItem
from models import Payment, PaymentMethod, Review
from forms import ProfileForm, CheckoutForm, ReviewForm
from decimal import Decimal

customer_bp = Blueprint('customer', __name__)


def customer_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.Role != 'Customer':
            flash('Customer access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def get_customer():
    return Customer.query.filter_by(UserID=current_user.UserID).first()


# ── Dashboard ────────────────────────────────────────────────────────────────
@customer_bp.route('/dashboard')
@login_required
@customer_required
def dashboard():
    customer = get_customer()
    orders   = Order.query.filter_by(CustomerID=customer.CustomerID)\
                          .order_by(Order.OrderDate.desc()).limit(5).all()
    # Cart item count
    cart = ShoppingCart.query.filter_by(CustomerID=customer.CustomerID).first()
    cart_count = sum(i.Quantity for i in cart.items) if cart else 0
    return render_template('customer/dashboard.html', customer=customer,
                           orders=orders, cart_count=cart_count)


# ── Profile ───────────────────────────────────────────────────────────────────
@customer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@customer_required
def profile():
    customer = get_customer()
    form = ProfileForm(obj=customer)

    if form.validate_on_submit():
        customer.FullName = form.full_name.data
        current_user.Email = form.email.data
        customer.Phone    = form.phone.data
        customer.Address  = form.address.data
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('customer.profile'))

    form.full_name.data = customer.FullName
    form.email.data     = current_user.Email
    form.phone.data     = customer.Phone
    form.address.data   = customer.Address
    return render_template('customer/profile.html', form=form, customer=customer)


# ── Cart ──────────────────────────────────────────────────────────────────────
@customer_bp.route('/cart')
@login_required
@customer_required
def cart():
    customer = get_customer()
    cart = ShoppingCart.query.filter_by(CustomerID=customer.CustomerID).first()
    if not cart:
        cart = ShoppingCart(CustomerID=customer.CustomerID)
        db.session.add(cart)
        db.session.commit()

    subtotal = sum(item.product.Price * item.Quantity for item in cart.items)
    delivery_fee = Decimal('5.00')  # Convert to Decimal
    total = subtotal + delivery_fee
    return render_template('customer/cart.html', cart=cart, total=total, subtotal=subtotal, delivery_fee=delivery_fee)


@customer_bp.route('/cart/add/<int:pid>', methods=['POST'])
@login_required
@customer_required
def add_to_cart(pid):
    product  = Product.query.get_or_404(pid)
    customer = get_customer()
    qty      = int(request.form.get('quantity', 1))

    if product.Stock < qty:
        flash('Not enough stock available.', 'danger')
        return redirect(url_for('product_detail', pid=pid))

    cart = ShoppingCart.query.filter_by(CustomerID=customer.CustomerID).first()
    if not cart:
        cart = ShoppingCart(CustomerID=customer.CustomerID)
        db.session.add(cart)
        db.session.flush()

    # Check if already in cart
    item = CartItem.query.filter_by(CartID=cart.CartID, ProductID=pid).first()
    if item:
        item.Quantity += qty
    else:
        item = CartItem(CartID=cart.CartID, ProductID=pid, Quantity=qty)
        db.session.add(item)

    db.session.commit()
    flash(f'{product.ProductName} added to cart.', 'success')
    return redirect(url_for('customer.cart'))


@customer_bp.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
@customer_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('customer.cart'))


@customer_bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
@customer_required
def update_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    qty  = int(request.form.get('quantity', 1))
    if qty < 1:
        db.session.delete(item)
    else:
        item.Quantity = qty
    db.session.commit()
    flash('Cart updated.', 'info')
    return redirect(url_for('customer.cart'))


# ── Checkout ──────────────────────────────────────────────────────────────────
@customer_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
@customer_required
def checkout():
    customer = get_customer()
    cart     = ShoppingCart.query.filter_by(CustomerID=customer.CustomerID).first()

    if not cart or not cart.items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('customer.cart'))

    form = CheckoutForm()
    form.method_id.choices = [(m.MethodID, m.MethodName) for m in PaymentMethod.query.all()]
    subtotal = sum(item.product.Price * item.Quantity for item in cart.items)
    delivery_fee = Decimal('5.00')  # Convert to Decimal
    total = subtotal + delivery_fee

    if form.validate_on_submit():
        # Create order
        order = Order(
            CustomerID=customer.CustomerID,
            TotalAmount=total,
            DeliveryFee=delivery_fee,
            ShippingAddress=form.shipping_address.data,
            Status='Pending'
        )
        db.session.add(order)
        db.session.flush()

        # Add order items & reduce stock
        for item in cart.items:
            oi = OrderItem(
                OrderID=order.OrderID,
                ProductID=item.ProductID,
                Quantity=item.Quantity,
                UnitPrice=item.product.Price
            )
            item.product.Stock -= item.Quantity
            db.session.add(oi)

        # Create payment record
        payment = Payment(
            OrderID=order.OrderID,
            CustomerID=customer.CustomerID,
            MethodID=form.method_id.data,
            Amount=total,
            Status='Pending'
        )
        db.session.add(payment)

        # Clear cart
        for item in cart.items:
            db.session.delete(item)

        db.session.commit()
        flash('Order placed successfully! Payment is pending verification.', 'success')
        return redirect(url_for('customer.orders'))

    form.shipping_address.data = customer.Address
    return render_template('customer/checkout.html', form=form, cart=cart, total=total, subtotal=subtotal, delivery_fee=delivery_fee)


# ── Orders ────────────────────────────────────────────────────────────────────
@customer_bp.route('/orders')
@login_required
@customer_required
def orders():
    customer = get_customer()
    orders   = Order.query.filter_by(CustomerID=customer.CustomerID)\
                          .order_by(Order.OrderDate.desc()).all()
    return render_template('customer/orders.html', orders=orders)


@customer_bp.route('/orders/<int:oid>')
@login_required
@customer_required
def order_detail(oid):
    customer = get_customer()
    order    = Order.query.get_or_404(oid)
    if order.CustomerID != customer.CustomerID:
        flash('Access denied.', 'danger')
        return redirect(url_for('customer.orders'))
    return render_template('customer/order_detail.html', order=order)


# ── Payment History ───────────────────────────────────────────────────────────
@customer_bp.route('/payments')
@login_required
@customer_required
def payment_history():
    customer = get_customer()
    payments = Payment.query.filter_by(CustomerID=customer.CustomerID)\
                            .order_by(Payment.PaymentDate.desc()).all()
    return render_template('customer/payments.html', payments=payments)


# ── Reviews ───────────────────────────────────────────────────────────────────
@customer_bp.route('/reviews')
@login_required
@customer_required
def reviews():
    customer = get_customer()
    reviews  = Review.query.filter_by(CustomerID=customer.CustomerID)\
                           .order_by(Review.CreatedAt.desc()).all()
    return render_template('customer/reviews.html', reviews=reviews)


@customer_bp.route('/reviews/add/<int:pid>', methods=['GET', 'POST'])
@login_required
@customer_required
def add_review(pid):
    product  = Product.query.get_or_404(pid)
    customer = get_customer()
    form     = ReviewForm()

    # Check if customer already reviewed this product
    existing = Review.query.filter_by(ProductID=pid, CustomerID=customer.CustomerID).first()
    if existing:
        flash('You have already reviewed this product.', 'warning')
        return redirect(url_for('product_detail', pid=pid))

    if form.validate_on_submit():
        review = Review(
            ProductID=pid,
            CustomerID=customer.CustomerID,
            Rating=form.rating.data,
            Comment=form.comment.data,
            Status='Pending'
        )
        db.session.add(review)
        db.session.commit()
        flash('Review submitted and awaiting moderation.', 'success')
        return redirect(url_for('product_detail', pid=pid))

    return render_template('customer/add_review.html', form=form, product=product)
